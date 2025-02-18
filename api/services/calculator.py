import logging
from decimal import Decimal
from ..models import Setting, Tax, EbayStoreType
from .currency import CurrencyService

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
        # 固定送料
        self.shipping_cost = 3000
        # Payoneer手数料
        self.payoneer_fee = 2
        # 為替レートの取得
        self.exchange_rate = Decimal(str(CurrencyService.get_exchange_rate('USD', 'JPY')))
        if self.exchange_rate == 0:
            # APIからの取得に失敗した場合はデフォルトレートを使用
            self.exchange_rate = Decimal(str(CurrencyService.get_default_rate('USD', 'JPY')))

    def calc_price_yen(self, prices: list[int]) -> dict:
        """
        円での価格計算を行う

        Args:
            prices (list[int]): 計算対象の価格リスト

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
            # 価格の合計を計算
            total_price = sum(prices)
            
            # 各種レートの取得
            profit_rate = Decimal(str(self.settings.rate)) / 100
            ebay_fee = Decimal(str(self.ebay_store_type.final_value_fee)) / 100
            international_fee = Decimal(str(self.ebay_store_type.international_fee)) / 100
            tax_rate = Decimal(str(self.tax.rate)) / 100
            payoneer_fee = Decimal(str(self.payoneer_fee)) / 100

            # 販売価格の計算（利益がX%になる計算）
            # ((仕入れ価格+送料)×(1+利益率))÷(1−(eBay手数料+国際手数料+消費税+Payoneer手数料))
            denominator = 1 - (ebay_fee + international_fee + tax_rate + payoneer_fee)
            if denominator <= 0:
                raise ValueError("手数料合計が100%を超えているため、計算できません。")
            
            numerator = (total_price + self.shipping_cost) * (1 + profit_rate)
            calculated_price = int(numerator / denominator)

            # 最終利益
            a = (calculated_price * (1 + tax_rate)) * ebay_fee
            b = (calculated_price * (1 + tax_rate)) * international_fee
            c = (a + b) * (1 + tax_rate)
            d = calculated_price - total_price - c - self.shipping_cost
            final_profit = d - (d * payoneer_fee)

            return {
                'original_price': total_price,
                'shipping_cost': self.shipping_cost,
                'rate': float(profit_rate),
                'ebay_fee': float(ebay_fee),
                'international_fee': float(international_fee),
                'tax_rate': float(tax_rate),
                'calculated_price_yen': calculated_price,
                'calculated_price_dollar': None,
                'exchange_rate': None,
                'final_profit_yen': int(final_profit),
                'final_profit_dollar': None
            }
        except Exception as e:
            logger.error(f"価格計算エラー: {str(e)}")
            raise

    def calc_price_dollar(self, prices: list[int]) -> dict:
        """
        ドルでの価格計算を行う

        Args:
            prices (list[int]): 計算対象の価格リスト

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
            yen_result = self.calc_price_yen(prices)
            
            # ドル換算
            calculated_price_dollar = int(yen_result['calculated_price_yen'] / self.exchange_rate)
            final_profit_dollar = int(yen_result['final_profit_yen'] / self.exchange_rate)

            return {
                'original_price': yen_result['original_price'],
                'shipping_cost': self.shipping_cost,
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

    def calc_profit_from_dollar(self, price: Decimal, original_prices: list[int]) -> dict:
        """
        ドル価格から最終利益を計算する

        Args:
            price (int): 計算対象のドル価格
            original_prices (list[int]): 仕入れ価格リスト（円）

        Returns:
            dict: 計算結果
        """
        try:
            # 各種レートの取得
            ebay_fee = Decimal(str(self.ebay_store_type.final_value_fee)) / 100
            international_fee = Decimal(str(self.ebay_store_type.international_fee)) / 100
            tax_rate = Decimal(str(self.tax.rate)) / 100
            payoneer_fee = Decimal(str(self.payoneer_fee)) / 100
            profit_rate = Decimal(str(self.settings.rate)) / 100

            # 仕入れ価格の合計
            total_original_price = sum(original_prices)

            # ドル価格の合計を計算
            total_price_dollar = price
            # 円に換算
            total_price_yen = total_price_dollar * self.exchange_rate
            # 手数料と税金の計算
            ebay_fee_amount = total_price_yen * ebay_fee
            international_fee_amount = total_price_yen * international_fee
            tax_amount = (ebay_fee_amount + international_fee_amount) * tax_rate
            # 最終利益の計算（円）- 仕入れ価格を考慮
            final_profit_yen = total_price_yen - ebay_fee_amount - international_fee_amount - tax_amount - total_original_price - self.shipping_cost
            final_profit_yen = final_profit_yen - (final_profit_yen * payoneer_fee)
            # ドルでの最終利益
            final_profit_dollar = int(final_profit_yen / self.exchange_rate)

            return {
                'original_price': total_original_price,
                'shipping_cost': self.shipping_cost,
                'rate': float(profit_rate),
                'ebay_fee': float(ebay_fee),
                'international_fee': float(international_fee),
                'tax_rate': float(tax_rate),
                'calculated_price_yen': total_price_yen,
                'calculated_price_dollar': total_price_dollar,
                'exchange_rate': float(self.exchange_rate),
                'final_profit_yen': int(final_profit_yen),
                'final_profit_dollar': final_profit_dollar
            }

        except Exception as e:
            logger.error(f"ドル価格からの利益計算エラー: {str(e)}")
            raise 