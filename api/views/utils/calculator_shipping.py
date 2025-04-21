from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from api.services.shipping_calculator import ShippingCalculator
from api.models.master import CountriesFedex
from api.utils.throttles import AuctionDetailThrottle
from api.serializers.shipping import (
    CountrySerializer,
    ShippingCalculatorRequestSerializer,
    ShippingRateResponseSerializer
)

class CalculatorShippingView(APIView):
    throttle_classes = [AuctionDetailThrottle]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def get(self, request):
        """利用可能な国のリストを取得"""
        try:
            # 利用可能な国コードをログに出力
            fedex_countries = CountriesFedex.objects.all().values('code', 'name_ja')
            print(f"利用可能なFedEx国リスト: {[c['code'] for c in fedex_countries]}")
            
            countries_data = [{'code': country['code'], 'name': country['name_ja']} for country in fedex_countries]
            return Response({
                'success': True,
                'message': 'データの取得に成功しました',
                'data': {
                    'countries': countries_data
                }
            })
        except Exception as e:
            import traceback
            print(f"国リスト取得エラー: {str(e)}")
            print(traceback.format_exc())
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """送料を計算"""
        print(f"リクエストデータ: {request.data}")
        print(f"リクエストのContent-Type: {request.content_type}")
        
        serializer = ShippingCalculatorRequestSerializer(data=request.data)
        if not serializer.is_valid():
            print(f"シリアライザエラー: {serializer.errors}")
            return Response({
                'success': False,
                'error': serializer.errors,
                'received_data': request.data
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            validated_data = serializer.validated_data
            country_code = validated_data['country_code']
            weight = validated_data['weight']
            length = validated_data.get('length', 0)
            width = validated_data.get('width', 0)
            height = validated_data.get('height', 0)
            is_document = validated_data.get('is_document', False)
            
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

        except Exception as e:
            import traceback
            print(f"エラー詳細: {traceback.format_exc()}")
            return Response({
                'success': False,
                'error': f'予期せぬエラーが発生しました: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 