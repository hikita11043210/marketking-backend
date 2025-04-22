from rest_framework.views import APIView
from rest_framework.response import Response
from api.services.ebay.offer import Offer
from api.models.ebay import Ebay
from api.models.master import Status
from api.common.response_helpers import create_success_response, create_error_response

class OfferView(APIView):
    def post(self, request):
        try:
            # リクエストデータを取得
            action = request.data['action']
            offer_id = request.data['offer_id']
            sku = request.data['sku']

            # サービスを初期化
            offer_service = Offer(request.user)
            ebay_register_item = Ebay.objects.get(sku=sku)
            
            # アクションに応じて処理を分岐
            if action == "publish":
                # 終了済み商品があれば削除
                if ebay_register_item.item_id:
                    offer_service.delete_ended_item(ebay_register_item.item_id)
                
                # 出品・再出品
                result = offer_service.publish_offer(offer_id)
                
                # 新しいitem_idを保存
                ebay_register_item.item_id = result.get('listingId')
                ebay_register_item.status = Status.objects.get(id=1)
                
            elif action == "withdraw":
                # 取消し
                withdraw_result = offer_service.withdraw_offer(offer_id)
                
                # 「終了済み」に変更
                if ebay_register_item.item_id:
                    offer_service.end_fixed_price_item(ebay_register_item.item_id)
                    
                ebay_register_item.status = Status.objects.get(id=2)

            ebay_register_item.save()

        except Exception as e:
            return create_error_response(str(e))

        return create_success_response(None)