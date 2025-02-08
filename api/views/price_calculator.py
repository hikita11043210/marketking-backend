from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..services.price_calculator import PriceCalculatorService
from rest_framework.permissions import IsAuthenticated

class PriceCalculatorView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        価格計算を実行する

        Request Body:
            - prices: list[int] - 計算対象の価格リスト
            - currency: str - 計算対象の通貨（"yen" or "dollar"）

        Returns:
            計算結果
        """
        try:
            prices = request.data.get('prices', [])
            currency = request.data.get('currency', 'yen')

            if not isinstance(prices, list):
                return Response(
                    {'error': '価格は配列で指定してください'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 数値以外の要素をチェック
            if not all(isinstance(price, (int, float)) for price in prices):
                return Response(
                    {'error': '価格は数値で指定してください'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            service = PriceCalculatorService()
            
            if currency.lower() == 'dollar':
                result = service.calc_price_dollar(prices)
            else:
                result = service.calc_price_yen(prices)

            return Response(result)

        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': '計算中にエラーが発生しました'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 