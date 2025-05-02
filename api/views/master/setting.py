from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ...models.master import Setting, EbayStoreType
from ...serializers.setting import SettingSerializer

class SettingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """設定を取得"""
        try:
            setting = Setting.get_settings(request.user)
            ebay_store_types = EbayStoreType.objects.all().order_by('id').values('id', 'store_type')
            
            return Response({
                'success': True,
                'message': '設定の取得に成功しました',
                'data': {
                    'yahoo_client_id': setting.yahoo_client_id or '',
                    'yahoo_client_secret': setting.yahoo_client_secret or '',
                    'ebay_client_id': setting.ebay_client_id or '',
                    'ebay_dev_id': setting.ebay_dev_id or '',
                    'ebay_client_secret': setting.ebay_client_secret or '',
                    'ebay_store_type_id': setting.ebay_store_type.id if setting.ebay_store_type else None,
                    'rate': setting.rate or 0,
                    'deepl_api_key': setting.deepl_api_key or '',
                    'created_at': setting.created_at.isoformat() if setting.created_at else '',
                    'updated_at': setting.updated_at.isoformat() if setting.updated_at else '',
                    'ebay_store_types': list(ebay_store_types)
                }
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        """設定を更新"""
        try:
            setting = Setting.get_settings(request.user)

            # 更新するフィールドのみを処理
            for field in ['yahoo_client_id', 'yahoo_client_secret', 'ebay_client_id', 'ebay_client_secret', 
                         'ebay_dev_id', 'rate', 'deepl_api_key', 'ebay_store_type_id']:
                if field in request.data:
                    setattr(setting, field, request.data[field])
            
            setting.save()

            return Response({
                'success': True,
                'message': '設定の更新に成功しました',
                'data': {
                    'yahoo_client_id': setting.yahoo_client_id,
                    'yahoo_client_secret': setting.yahoo_client_secret,
                    'ebay_client_id': setting.ebay_client_id,
                    'ebay_dev_id': setting.ebay_dev_id,
                    'ebay_client_secret': setting.ebay_client_secret,
                    'ebay_store_type_id': setting.ebay_store_type_id,
                    'rate': setting.rate,
                    'deepl_api_key': setting.deepl_api_key,
                    'created_at': setting.created_at.isoformat(),
                    'updated_at': setting.updated_at.isoformat()
                }
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 