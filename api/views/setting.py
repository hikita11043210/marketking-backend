from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.master import Setting
from ..serializers.setting import SettingSerializer

class SettingAPIView(APIView):
    def get(self, request):
        """設定を取得"""
        try:
            setting = Setting.get_settings()
            return Response({
                'success': True,
                'message': '設定の取得に成功しました',
                'data': {
                    'yahoo_client_id': setting.yahoo_client_id,
                    'yahoo_client_secret': setting.yahoo_client_secret,
                    'ebay_client_id': setting.ebay_client_id,
                    'ebay_dev_id': setting.ebay_dev_id,
                    'ebay_client_secret': setting.ebay_client_secret,
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

    def put(self, request):
        """設定を更新"""
        try:
            setting = Setting.get_settings()

            # 更新するフィールドのみを処理
            for field in ['yahoo_client_id', 'yahoo_client_secret', 'ebay_client_id', 'ebay_client_secret', 'ebay_dev_id', 'rate', 'deepl_api_key']:
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