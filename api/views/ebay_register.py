from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.services.ebay_searvices import EbayService
from api.models.ebay import EbayRegisterFromYahooAuction
from api.models.master import Status
from api.utils.throttles import AuctionDetailThrottle
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class EbayRegisterView(APIView):
    """eBayに商品を出品するView"""
    permission_classes = [IsAuthenticated]
    throttle_classes = [AuctionDetailThrottle]

    def post(self, request):
        """
        eBayに商品を出品するエンドポイント
        """
        try:
            # リクエストデータのバリデーション
            # required_fields = ['availability', 'condition', 'product', 'yahoo_auction_data']
            # for field in required_fields:
            #     if field not in request.data:
            #         return Response(
            #             {'success': False, 'message': f'{field}は必須フィールドです'},
            #             status=status.HTTP_400_BAD_REQUEST
            #         )

            # SKUの生成（yahoo_auction_idを使用）
            register_data = request.data['register_data']
            sku = f"YA_{register_data['auction_id']}"
            print(register_data)

            return Response(
                {'success': True, 'message': '商品情報の取得に成功しました'},
                status=status.HTTP_200_OK
            )

            # 商品情報の構築
            product_data = {
                "availability": {
                    "shipToLocationAvailability": {
                        "quantity": 10
                    }
                },
                "condition": "NEW",
                "product": {
                    "title": "商品タイトル",
                    "description": "商品説明",
                    "aspects": {
                        "ブランド": ["ブランド名"],
                        "サイズ": ["M"]
                    },
                    "imageUrls": ["画像URL1", "画像URL2"]
                }
            }


            # EbayServiceのインスタンス化
            ebay_service = EbayService(request.user)

            # 1. 商品情報の登録
            inventory_result = ebay_service.create_inventory_item(
                sku,
                product_data
            )

            # 2. 出品情報の作成（価格などの情報を自動設定）
            offer_data = {
                'sku': sku,
                'marketplaceId': 'EBAY_JP',
                'format': 'FIXED_PRICE',
                'availableQuantity': product_data['availability']['shipToLocationAvailability']['quantity'],
                'categoryId': register_data.get('category_id', ''),
                'listingDescription': product_data['product']['description'],
                'pricingSummary': {
                    'price': {
                        'value': str(register_data['ebay_price']),
                        'currency': 'JPY'
                    }
                }
            }

            offer_result = ebay_service.create_offer(offer_data)
            offer_id = offer_result['data']['offerId']

            # 3. 出品のアクティブ化
            publish_result = ebay_service.publish_offer(offer_id)

            # 4. EbayRegisterFromYahooAuctionにデータを保存
            # ステータスの取得（例：'登録済み'のステータス）
            status_obj = Status.objects.get(id=1)

            # データの保存
            register_data = EbayRegisterFromYahooAuction.objects.create(
                user=request.user,
                sku=sku,
                status=status_obj,
                ebay_price=Decimal(str(register_data['ebay_price'])),
                ebay_shipping_price=Decimal(str(register_data.get('ebay_shipping_price', '0'))),
                final_profit=Decimal(str(register_data.get('final_profit', '0'))),
                yahoo_auction_id=register_data['auction_id'],
                yahoo_auction_item_name=register_data['item_name'],
                yahoo_auction_item_price=Decimal(str(register_data['item_price'])),
                yahoo_auction_shipping=Decimal(str(register_data['shipping_price'])),
                yahoo_auction_end_time=register_data['end_time']
            )

            return Response({
                'success': True,
                'message': '商品の出品が完了しました',
                'data': {
                    'inventory': inventory_result.get('data'),
                    'offer': offer_result.get('data'),
                    'listing': publish_result.get('data'),
                    'register_id': register_data.id
                }
            }, status=status.HTTP_200_OK)

        except Status.DoesNotExist:
            logger.error("Status '登録済み' not found")
            return Response(
                {'success': False, 'message': 'ステータスの取得に失敗しました'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error(f"Failed to register item on eBay: {str(e)}")
            return Response(
                {'success': False, 'message': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )