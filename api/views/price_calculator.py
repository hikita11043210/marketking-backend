from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..services.price_calculator import PriceCalculatorService
from rest_framework.permissions import IsAuthenticated
import logging

logger = logging.getLogger(__name__)

class PriceCalculatorView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        価格計算を実行する（GETリクエスト用）

        Query Parameters:
            - money[]: list[str] - 計算対象の価格リスト
            - currency: str - 計算対象の通貨（"yen" or "dollar"）

        Returns:
            ApiResponse形式の計算結果
            {
                success: boolean,
                message?: string,
                data?: object
            }
        """
        try:
            # クエリパラメータから価格リストを取得
            money_list = request.query_params.getlist('money[]', [])
            currency = request.query_params.get('currency', 'dollar')

            if not money_list:
                return Response(
                    {
                        'success': False,
                        'message': '価格が指定されていません'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 文字列を数値に変換
            try:
                prices = [int(price) for price in money_list]
            except ValueError:
                return Response(
                    {
                        'success': False,
                        'message': '価格は数値で指定してください'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            service = PriceCalculatorService(request.user)
            
            if currency.lower() == 'dollar':
                result = service.calc_price_dollar(prices)
            else:
                result = service.calc_price_yen(prices)

            return Response({
                'success': True,
                'data': result
            })

        except ValueError as e:
            return Response(
                {
                    'success': False,
                    'message': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"価格計算エラー: {str(e)}")
            return Response(
                {
                    'success': False,
                    'message': '計算中にエラーが発生しました'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
