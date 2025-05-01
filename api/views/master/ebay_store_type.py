from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ...models.master import EbayStoreType, Setting
from ...serializers.ebay_store_type import EbayStoreTypeSerializer

class EbayStoreTypeAPIView(APIView):
    """
    eBayストアタイプのマスターデータを取得するAPIビュー
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        eBayストアタイプの一覧と、ユーザーが設定しているストアタイプを取得する
        """
        try:
            # すべてのeBayストアタイプを取得
            ebay_store_types = EbayStoreType.objects.all().order_by('id')
            
            # 現在のユーザーの設定を取得
            setting = Setting.get_settings(request.user)
            current_store_type_id = setting.ebay_store_type.id if setting.ebay_store_type else None
            
            # シリアライザーを使用してデータをシリアライズ
            serializer = EbayStoreTypeSerializer(ebay_store_types, many=True)
            store_types_data = serializer.data
            
            # 現在選択されているストアタイプの情報を追加
            for store_type in store_types_data:
                store_type['is_current'] = store_type['id'] == current_store_type_id
            
            return Response({
                'success': True,
                'message': 'eBayストアタイプの取得に成功しました',
                'data': {
                    'store_types': store_types_data,
                    'current_store_type_id': current_store_type_id
                }
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': f'eBayストアタイプの取得に失敗しました: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CurrentEbayStoreTypeAPIView(APIView):
    """
    ユーザーが現在選択しているeBayストアタイプを取得するAPIビュー
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        ユーザーが現在選択しているeBayストアタイプの情報のみを取得する
        """
        try:
            # ユーザーの設定を取得
            setting = Setting.get_settings(request.user)
            
            # 設定されたストアタイプがない場合
            if not setting.ebay_store_type:
                return Response({
                    'success': True,
                    'message': 'eBayストアタイプが設定されていません',
                    'data': {
                        'store_type': None,
                        'rate': None
                    }
                })
            
            # 現在のストアタイプをシリアライズ
            serializer = EbayStoreTypeSerializer(setting.ebay_store_type)
            
            return Response({
                'success': True,
                'message': '現在のeBayストアタイプの取得に成功しました',
                'data': {
                    'store_type': serializer.data,
                    'rate': setting.rate
                }
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': f'eBayストアタイプの取得に失敗しました: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 