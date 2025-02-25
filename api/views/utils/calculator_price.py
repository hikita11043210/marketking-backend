from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...services.calculator import CalculatorService
from rest_framework.permissions import IsAuthenticated
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

class CalculatorPriceView(APIView):
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

            service = CalculatorService(request.user)
            
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


    def post(self, request):
        """
        ドル価格から最終利益を計算する

        Request Body:
            - prices: list[int] - 計算対象のドル価格リスト

        Returns:
            ApiResponse形式の計算結果
            {
                success: boolean,
                message?: string,
                data?: object
            }
        """
        try:
            price = request.data.get('price')
            original_prices = request.data.get('money', [])

            # 文字列を数値に変換
            try:
                original_prices = [int(price) for price in original_prices]
            except ValueError:
                return Response(
                    {
                        'success': False,
                        'message': '仕入値は数値で指定してください'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                price = Decimal(price)
            except ValueError:
                return Response(
                    {
                        'success': False,
                        'message': '価格は数値で指定してください'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            service = CalculatorService(request.user)
            result = service.calc_profit_from_dollar(price, original_prices)

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

