from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services.shipping_calculator import ShippingCalculator
from api.models.master import CountriesFedex, CountriesDhl, CountriesEconomy
from api.utils.throttles import AuctionDetailThrottle

class CalculatorShippingView(APIView):
    throttle_classes = [AuctionDetailThrottle]

    def get(self, request):
        """利用可能な国のリストを取得"""
        try:
            countries = CountriesFedex.objects.all().values('code', 'name')
            return Response({
                'success': True,
                'message': 'データの取得に成功しました',
                'data': {
                    'countries': list(countries)
                }
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """送料を計算"""
        try:
            country_code = request.data.get('country_code')
            weight = float(request.data.get('weight', 0))
            length = int(request.data.get('length', 0))
            width = int(request.data.get('width', 0))
            height = int(request.data.get('height', 0))
            is_document = request.data.get('is_document', False)
            
            # 入力値の検証
            if not all([country_code, weight]):
                return Response({
                    'success': False,
                    'error': '必要なパラメータが不足しています'
                }, status=status.HTTP_400_BAD_REQUEST)

            calculator = ShippingCalculator()
            result = calculator.calculate_shipping_cost(
                country_code, weight, length, width, height, is_document
            )

            if result['success']:
                return Response(result)
            else:
                return Response({
                    'success': False,
                    'error': result.get('error', '計算に失敗しました')
                }, status=status.HTTP_400_BAD_REQUEST)

        except (ValueError, TypeError) as e:
            return Response({
                'success': False,
                'error': f'入力値が不正です: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'error': f'予期せぬエラーが発生しました: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 