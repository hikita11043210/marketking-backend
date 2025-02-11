import logging
from decimal import Decimal
from ..models import Setting

logger = logging.getLogger(__name__)

class PriceCalculatorService:
    def __init__(self, user):
        self.user = user
        self.settings = Setting.get_settings(user)
        if not self.settings:
            raise ValueError("設定が見つかりません。")

    def calc_price_yen(self, prices: list[int]) -> dict:
        """
        円での価格計算を行う

        Args:
            prices (list[int]): 計算対象の価格リスト

        Returns:
            dict: 計算結果
                - original_price: 元の価格の合計
                - rate: 適用レート
                - calculated_price: レート適用後の価格
        """
        try:
            # 価格の合計を計算
            total_price = sum(prices)
            
            # レートを適用
            rate = int(self.settings.rate)
            if rate is None:
                rate = 20
            rate = rate / 100 + 1
            calculated_price = int(total_price * rate)

            return {
                'original_price': total_price,
                'rate': float(rate),
                'calculated_price': calculated_price
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
                - original_price: 元の価格の合計（円）
                - rate: 適用レート
                - calculated_price_yen: レート適用後の価格（円）
                - exchange_rate: 為替レート
                - calculated_price_dollar: ドル換算後の価格
        """
        try:
            # 円での計算を実行
            yen_result = self.calc_price_yen(prices)
            
            # ドル換算
            exchange_rate = Decimal(str(self.settings.exchange_rate))
            calculated_price_dollar = int(yen_result['calculated_price'] / exchange_rate)

            return {
                'original_price': yen_result['original_price'],
                'rate': yen_result['rate'],
                'calculated_price_yen': yen_result['calculated_price'],
                'exchange_rate': float(exchange_rate),
                'calculated_price_dollar': calculated_price_dollar
            }
        except Exception as e:
            logger.error(f"ドル換算エラー: {str(e)}")
            raise 