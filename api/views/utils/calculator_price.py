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
            - purchase_price: int - 仕入れ価格
            - purchase_shipping_price: int - 仕入れ送料
            - ebay_shipping_cost: int - eBay送料
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
            purchase_price = request.query_params.get('purchase_price', 0)
            purchase_shipping_price = request.query_params.get('purchase_shipping_price', 0)
            ebay_shipping_cost = request.query_params.get('ebay_shipping_cost', 0)
            currency = request.query_params.get('currency', 'dollar')

            if not purchase_price:
                return Response(
                    {
                        'success': False,
                        'message': '価格が指定されていません'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 文字列を数値に変換
            try:
                purchase_price = int(purchase_price)
                purchase_shipping_price = int(purchase_shipping_price)
                ebay_shipping_cost = int(ebay_shipping_cost)
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
                result = service.calc_price_dollar(purchase_price, purchase_shipping_price, ebay_shipping_cost)
            else:
                result = service.calc_price_yen(purchase_price, purchase_shipping_price, ebay_shipping_cost)

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
            logger.error(f"価格計算エラー2: {str(e)}")
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
            input_price = request.data.get('input_price')
            purchase_price = request.data.get('purchasePrice')
            purchase_shipping_price = request.data.get('purchaseShipping')
            ebay_shipping_cost = request.data.get('shippingCost')

            # 文字列を数値に変換
            try:
                input_price = int(input_price)
                purchase_price = int(purchase_price)
                purchase_shipping_price = int(purchase_shipping_price)
                ebay_shipping_cost = int(ebay_shipping_cost)
            except ValueError:
                return Response(
                    {
                        'success': False,
                        'message': '仕入値は数値で指定してください'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            service = CalculatorService(request.user)
            result = service.calc_profit_from_dollar(input_price, purchase_price, purchase_shipping_price, ebay_shipping_cost)

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
            logger.error(f"価格計算エラー3: {str(e)}")
            return Response(
                {
                    'success': False,
                    'message': '計算中にエラーが発生しました'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

