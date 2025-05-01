import logging
from decimal import Decimal
from ..models import Setting, Tax, EbayStoreType
from .currency import CurrencyService
from django.conf import settings

logger = logging.getLogger(__name__)

class CalculatorService:
    def __init__(self, user):
        self.user = user
        self.settings = Setting.get_settings(user)
        if not self.settings:
            raise ValueError("設定が見つかりません。")
        # eBayストアタイプの取得
        self.ebay_store_type = self.settings.ebay_store_type
        # 消費税の取得（id=1の税率を使用）
        self.tax = Tax.objects.get(id=1)
        # 送料
        self.shipping_cost = 0
        # Payoneer手数料
        self.payoneer_fee = 2
        # 為替レートの取得
        self.exchange_rate = Decimal(str(CurrencyService.get_exchange_rate('USD', 'JPY')))
        if self.exchange_rate == 0:
            # APIからの取得に失敗した場合はデフォルトレートを使用
            self.exchange_rate = Decimal(str(CurrencyService.get_default_rate('USD', 'JPY')))

    def calc_price_yen(self, purchase_price: int = 0, purchase_shipping_price: int = 0, ebay_shipping_cost: int = 0) -> dict:
        """
        円での価格計算を行う

        Args:
            purchase_price (int): 計算対象の価格
            purchase_shipping_price (int): 仕入れ送料
            ebay_shipping_cost (int): eBay送料

        Returns:
            dict: 計算結果
                - original_price: 元の価格の合計
                - shipping_cost: 送料
                - rate: 適用レート
                - ebay_fee: eBay手数料率
                - international_fee: 国際手数料率
                - tax_rate: 消費税率
                - calculated_price_yen: 円での計算価格
                - calculated_price_dollar: ドルでの計算価格
                - exchange_rate: 為替レート
                - final_profit_yen: 円での最終利益
                - final_profit_dollar: ドルでの最終利益
        """
        try:
            # 仕入価格の合計
            purchase_total_price = purchase_price + purchase_shipping_price
            
            # 各種レートの取得
            profit_rate = Decimal(str(self.settings.rate)) / 100                            # 利益率
            ebay_fee = Decimal(str(self.ebay_store_type.final_value_fee)) / 100             # eBay手数料率
            international_fee = Decimal(str(self.ebay_store_type.international_fee)) / 100  # 国際手数料率
            tax_rate = Decimal(str(self.tax.rate)) / 100                                    # 消費税率
            payoneer_fee = Decimal(str(self.payoneer_fee)) / 100                            # Payoneer手数料率

            # 目標とするeBay利益（仕入価格に利益率を掛けた金額）
            target_profit = purchase_total_price * profit_rate

            # 販売価格の計算（利益がtarget_profitになるように逆算）
            # ebay税込販売価格 = 販売価格 * (1 + 消費税)
            # 最終販売手数料 = ebay税込販売価格 * ebay_fee
            # 国際手数料 = ebay税込販売価格 * international_fee
            # 粗利1 = 販売価格 - 最終販売手数料 - 国際手数料
            # 粗利2 = 粗利1 - payoneer_fee
            # ebay利益 = 粗利2 - 送料 = target_profit

            # 方程式を解いて販売価格を求める
            # 税込手数料率の計算
            tax_included_ebay_fee = ebay_fee * (1 + tax_rate)
            tax_included_international_fee = international_fee * (1 + tax_rate)
            
            # 総手数料率の計算
            total_fee_rate = tax_included_ebay_fee + tax_included_international_fee + payoneer_fee
            denominator = 1 - total_fee_rate
            
            if denominator <= 0:
                raise ValueError("手数料合計が100%を超えているため、計算できません。")
            
            calculated_price = int((target_profit + purchase_total_price + ebay_shipping_cost) / denominator)

            # 最終利益の検証計算
            # 1. 税込販売価格の計算
            tax_included_price = calculated_price * (1 + tax_rate)
            # 2. 各手数料の計算
            ebay_fee_amount = tax_included_price * ebay_fee
            international_fee_amount = tax_included_price * international_fee
            payoneer_fee_amount = calculated_price * payoneer_fee
            # 3. 総コストの計算
            total_cost = purchase_total_price + ebay_fee_amount + international_fee_amount + payoneer_fee_amount + ebay_shipping_cost
            # 4. 最終利益の計算
            final_profit = calculated_price - total_cost

            return {
                'original_price': purchase_total_price,
                'shipping_cost': ebay_shipping_cost,
                'rate': float(profit_rate),
                'ebay_fee': float(ebay_fee),
                'international_fee': float(international_fee),
                'tax_rate': float(tax_rate),
                'calculated_price_yen': calculated_price,
                'calculated_price_dollar': None,
                'exchange_rate': float(self.exchange_rate),
                'final_profit_yen': int(final_profit),
                'final_profit_dollar': None
            }
        except Exception as e:
            logger.error(f"価格計算エラー1: {str(e)}")
            raise

    def calc_price_dollar(self, purchase_price: int = 0, purchase_shipping_price: int = 0, ebay_shipping_cost: int = 0) -> dict:
        """
        ドルでの価格計算を行う

        Args:
            purchase_price (int): 計算対象の価格
            purchase_shipping_price (int): 仕入れ送料
            ebay_shipping_cost (int): eBay送料

        Returns:
            dict: 計算結果
                - original_price: 元の価格の合計
                - shipping_cost: 送料
                - rate: 適用レート
                - ebay_fee: eBay手数料率
                - international_fee: 国際手数料率
                - tax_rate: 消費税率
                - calculated_price_yen: 円での計算価格
                - calculated_price_dollar: ドルでの計算価格
                - exchange_rate: 為替レート
                - final_profit_yen: 円での最終利益
                - final_profit_dollar: ドルでの最終利益
        """
        try:
            # 円での計算を実行
            yen_result = self.calc_price_yen(purchase_price, purchase_shipping_price, ebay_shipping_cost)
            
            # ドル換算（小数点以下切り捨て）
            calculated_price_dollar = int(yen_result['calculated_price_yen'] / self.exchange_rate)
            final_profit_dollar = int(yen_result['final_profit_yen'] / self.exchange_rate)

            return {
                'original_price': yen_result['original_price'],
                'shipping_cost': ebay_shipping_cost,
                'rate': yen_result['rate'],
                'ebay_fee': yen_result['ebay_fee'],
                'international_fee': yen_result['international_fee'],
                'tax_rate': yen_result['tax_rate'],
                'calculated_price_yen': yen_result['calculated_price_yen'],
                'calculated_price_dollar': calculated_price_dollar,
                'exchange_rate': float(self.exchange_rate),
                'final_profit_yen': yen_result['final_profit_yen'],
                'final_profit_dollar': final_profit_dollar
            }
        except Exception as e:
            logger.error(f"ドル換算エラー: {str(e)}")
            raise

    def calc_profit_from_dollar(self, input_price: int = 0, purchase_price: int = 0, purchase_shipping_price: int = 0, ebay_shipping_cost: int = 0) -> dict:
        """
        ドル価格から最終利益を計算する

        Args:
            input_price (int): 計算対象のドル価格
            purchase_price (int): 仕入れ価格（円）
            purchase_shipping_price (int): 仕入れ送料
            ebay_shipping_cost (int): eBay送料

        Returns:
            dict: 計算結果
        """
        try:
            # 各種レートの取得
            profit_rate = Decimal(str(self.settings.rate)) / 100
            ebay_fee = Decimal(str(self.ebay_store_type.final_value_fee)) / 100
            international_fee = Decimal(str(self.ebay_store_type.international_fee)) / 100
            tax_rate = Decimal(str(self.tax.rate)) / 100
            payoneer_fee = Decimal(str(self.payoneer_fee)) / 100

            # 仕入れ価格の合計
            total_original_price = purchase_price + purchase_shipping_price

            # ドル価格を円に換算
            calculated_price = int(input_price * self.exchange_rate)

            # 最終利益の計算
            # 1. 販売価格から手数料を引く
            ebay_fee_amount = calculated_price * ebay_fee
            international_fee_amount = calculated_price * international_fee
            total_fee = ebay_fee_amount + international_fee_amount
            
            # 2. 手数料に対する消費税を計算（手数料にのみ適用）
            tax_on_fee = total_fee * tax_rate
            
            # 3. 最終利益の計算
            # 販売価格 - 仕入れ価格 - 送料 - 手数料 - 手数料の消費税
            gross_profit = calculated_price - total_original_price - ebay_shipping_cost - total_fee - tax_on_fee
            
            # 4. Payoneer手数料を引く
            final_profit_yen = gross_profit - (gross_profit * payoneer_fee)
            
            # ドルでの最終利益（小数点以下切り捨て）
            final_profit_dollar = int(final_profit_yen / self.exchange_rate)

            return {
                'original_price': total_original_price,
                'shipping_cost': ebay_shipping_cost,
                'rate': float(profit_rate),
                'ebay_fee': float(ebay_fee),
                'international_fee': float(international_fee),
                'tax_rate': float(tax_rate),
                'calculated_price_yen': calculated_price,
                'calculated_price_dollar': input_price,
                'exchange_rate': float(self.exchange_rate),
                'final_profit_yen': int(final_profit_yen),
                'final_profit_dollar': final_profit_dollar
            }

        except Exception as e:
            logger.error(f"ドル価格からの利益計算エラー: {str(e)}")
            raise 