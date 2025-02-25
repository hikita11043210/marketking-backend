from rest_framework.views import APIView
from rest_framework.response import Response
from api.services.ebay.offer import Offer
from api.models.ebay import Ebay
from api.models.master import Status

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
                # 出品・再出品
                offer_service.publish_offer(offer_id)
                ebay_register_item.status = Status.objects.get(id=1)
            elif action == "withdraw":
                # 取消し
                offer_service.withdraw_offer(offer_id)
                ebay_register_item.status = Status.objects.get(id=2)

            ebay_register_item.save()

        except Exception as e:
            return Response({
                "Success": False,
                "message": str(e)
            })

        return Response({
            "Success": True,
            "message": None
        })