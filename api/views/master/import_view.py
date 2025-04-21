from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from ...services.master.import_service import ImportService
import logging

# ロガーの設定
logger = logging.getLogger(__name__)

class ImportShippingRatesAPIView(APIView):
    """マスターデータのインポートAPI"""
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        """
        マスターデータのインポート処理
        
        Parameters:
        - type: インポートするデータの種類（fedex, dhl, economy, countries）
        - file: アップロードするExcelファイル
        - country_code: Economyの場合のみ必須（国コード、例: US, GB, DE, AU）
        - carrier_type: Countriesの場合のみ必須（fedex または dhl）
        """
        try:
            logger.info("マスターデータのインポート処理を開始します")
            
            # インポートサービスのインスタンス化
            import_service = ImportService()
            
            # リクエストパラメータの取得
            import_type = request.data.get('type')
            file = request.FILES.get('file')
            
            # バリデーション
            if not import_type:
                logger.warning("インポートタイプが指定されていません")
                return Response({'error': 'インポートタイプを指定してください'}, status=status.HTTP_400_BAD_REQUEST)
            
            if not file:
                logger.warning("ファイルが指定されていません")
                return Response({'error': 'ファイルを指定してください'}, status=status.HTTP_400_BAD_REQUEST)
            
            # ファイル形式のチェック
            if not file.name.endswith('.xlsx'):
                logger.warning(f"不正なファイル形式です: {file.name}")
                return Response({'error': 'ファイル形式は.xlsxである必要があります'}, status=status.HTTP_400_BAD_REQUEST)
            
            # インポートタイプごとの処理
            if import_type == 'fedex':
                logger.info("FedEx送料マスターのインポート処理を開始します")
                result = import_service.import_fedex_rates(file)
            
            elif import_type == 'dhl':
                logger.info("DHL送料マスターのインポート処理を開始します")
                result = import_service.import_dhl_rates(file)
            
            elif import_type == 'economy':
                logger.info("エコノミー送料マスターのインポート処理を開始します")
                country_code = request.data.get('country_code')
                if not country_code:
                    logger.warning("国コードが指定されていません")
                    return Response({'error': 'エコノミー送料インポートには国コードが必要です'}, status=status.HTTP_400_BAD_REQUEST)
                
                result = import_service.import_economy_rates(file, country_code)
            
            elif import_type == 'countries':
                logger.info("国マスターのインポート処理を開始します")
                carrier_type = request.data.get('carrier_type')
                if not carrier_type:
                    logger.warning("キャリアタイプが指定されていません")
                    return Response({'error': '国マスターインポートにはキャリアタイプ（fedex または dhl）が必要です'}, status=status.HTTP_400_BAD_REQUEST)
                
                if carrier_type.lower() not in ['fedex', 'dhl']:
                    logger.warning(f"不正なキャリアタイプです: {carrier_type}")
                    return Response({'error': 'キャリアタイプは fedex または dhl である必要があります'}, status=status.HTTP_400_BAD_REQUEST)
                
                result = import_service.import_countries(file, carrier_type)
            
            else:
                logger.warning(f"不明なインポートタイプです: {import_type}")
                return Response({'error': '不明なインポートタイプです'}, status=status.HTTP_400_BAD_REQUEST)
            
            # 結果の返却
            if result['success']:
                logger.info(f"インポート処理が成功しました: {result['message']}")
                return Response(result, status=status.HTTP_200_OK)
            else:
                logger.error(f"インポート処理が失敗しました: {result['message']}")
                return Response({'error': result['message']}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            logger.error(f"インポート処理中に例外が発生しました: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return Response({'error': f'エラーが発生しました: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 