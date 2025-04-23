from rest_framework.views import APIView
from rest_framework.response import Response
from api.services.ebay.offer import Offer
from api.models.ebay import Ebay
from api.models.master import Status
from api.utils.response_helpers import create_success_response, create_error_response
from api.services.ebay.sku_manager import SKUManager
import logging

logger = logging.getLogger(__name__)

class OfferView(APIView):
    def post(self, request):
        try:
            # リクエストデータを取得
            action = request.data['action']
            offer_id = request.data['offer_id']
            sku = request.data['sku']

            # 必須パラメータのチェック
            if not sku:
                return create_error_response("SKUが指定されていません")
            
            if action != "withdraw" and not offer_id:
                return create_error_response("Offer IDが指定されていません")

            # サービスを初期化
            offer_service = Offer(request.user)
            sku_manager = SKUManager(request.user)
            
            try:
                ebay_register_item = Ebay.objects.get(sku=sku)
            except Ebay.DoesNotExist:
                return create_error_response(f"指定されたSKU({sku})の商品が見つかりません")
            
            # アクションに応じて処理を分岐
            if action == "publish":
                # 取下げ中の商品の場合は新しいSKUで再出品
                if ebay_register_item.status.id == 2:  # 終了済み状態
                    try:
                        logger.info(f"終了済み商品を新しいSKUで再出品します: SKU={sku}, offer_id={offer_id}")
                        result = sku_manager.republish_with_new_sku(ebay_register_item)
                        return create_success_response({
                            'message': '新しいSKUで再出品しました',
                            'old_sku': result['old_sku'],
                            'new_sku': result['new_sku'],
                            'new_item_id': result['new_item_id']
                        })
                    except Exception as republish_error:
                        logger.error(f"再出品に失敗しました: {str(republish_error)}")
                        return create_error_response(f"再出品に失敗しました: {str(republish_error)}")
                
                # 終了済み商品があれば削除
                if ebay_register_item.item_id:
                    offer_service.delete_ended_item(ebay_register_item.item_id)
                
                # 出品・再出品
                result = offer_service.publish_offer(offer_id)
                
                # 新しいitem_idを保存
                ebay_register_item.item_id = result.get('listingId')
                ebay_register_item.status = Status.objects.get(id=1)
                
            elif action == "withdraw":
                # 「終了済み」に変更
                if ebay_register_item.item_id:
                    offer_service.end_fixed_price_item(ebay_register_item.item_id)
                    
                ebay_register_item.status = Status.objects.get(id=2)
            
            elif action == "republish":
                # 明示的に再出品するアクション
                if not ebay_register_item.status.id == 2:  # 終了済みでない場合
                    return create_error_response("再出品は終了済み商品に対してのみ可能です")
                
                try:
                    result = sku_manager.republish_with_new_sku(ebay_register_item)
                    return create_success_response({
                        'message': '新しいSKUで再出品しました',
                        'old_sku': result['old_sku'],
                        'new_sku': result['new_sku'],
                        'new_item_id': result['new_item_id']
                    })
                except Exception as republish_error:
                    logger.error(f"再出品に失敗しました: {str(republish_error)}")
                    return create_error_response(f"再出品に失敗しました: {str(republish_error)}")
            
            else:
                return create_error_response(f"不明なアクション: {action}")

            ebay_register_item.save()
            return create_success_response({
                'message': '処理が完了しました',
                'action': action,
                'sku': sku,
                'status': ebay_register_item.status.id
            })

        except Exception as e:
            logger.error(f"オファー処理中にエラーが発生しました: {str(e)}")
            return create_error_response(str(e))


class SkuHistoryView(APIView):
    def get(self, request):
        """SKUの履歴を取得するAPI"""
        try:
            sku = request.query_params.get('sku')
            if not sku:
                return create_error_response("SKUが指定されていません")
            
            sku_manager = SKUManager(request.user)
            histories = sku_manager.get_sku_history(sku)
            
            history_data = []
            for history in histories:
                history_data.append({
                    'id': history.id,
                    'ebay_id': history.ebay_id,
                    'previous_sku': history.previous_sku,
                    'new_sku': history.new_sku,
                    'created_at': history.created_at.isoformat()
                })
            
            return create_success_response({
                'sku': sku,
                'histories': history_data,
                'count': len(history_data)
            })
            
        except Exception as e:
            logger.error(f"SKU履歴の取得中にエラーが発生しました: {str(e)}")
            return create_error_response(str(e))