from rest_framework.views import APIView
from api.utils.response_helpers import create_success_response, create_error_response
from api.models.ebay import EbayRegisterFromYahooAuction
from api.services.currency import CurrencyService
from decimal import Decimal
from api.services.ebay.offer import Offer
from api.utils.generate_log_file import generate_log_file
from api.services.ebay.inventory import Inventory

class List(APIView):
    def get(self, request):
        try:
            # 商品情報を取得
            ebay_register_items = EbayRegisterFromYahooAuction.objects.all()
            
            # # 出品情報を削除するためのインスタンスを生成
            # ebay_service_offer = Offer(request.user)
            # ebay_service_inventory = Inventory(request.user)
            # data = ebay_service_inventory.get_inventory_items()
            # generate_log_file(data, "data", time=False)
            # ebay_service_inventory.delete_inventory_item('YA_e1163351978_20250222024545')
            # # 出品情報を削除
            # for item in ebay_register_items:
            #     ebay_service_inventory.delete_inventory_item(item.sku) # ebayから削除

            # 一覧出力時の変換レートを取得
            rate = Decimal(str(CurrencyService.get_exchange_rate('USD', 'JPY')))

            # 一覧出力時のデータを作成
            response_data = [
                {
                    'id': item.id,
                    'status': item.status.status_name,
                    'sku': item.sku,
                    'offer_id': item.offer_id,
                    'ebay_price': int(item.ebay_price * rate),
                    'ebay_shipping_price': int(item.ebay_shipping_price),
                    'final_profit': int(item.final_profit * rate),
                    'yahoo_auction_id': item.yahoo_auction_id,
                    'yahoo_auction_url': item.yahoo_auction_url,
                    'yahoo_auction_item_name': item.yahoo_auction_item_name,
                    'yahoo_auction_item_price': str(item.yahoo_auction_item_price),
                    'yahoo_auction_shipping': str(item.yahoo_auction_shipping),
                    'purchase_price': int(item.yahoo_auction_item_price + item.yahoo_auction_shipping),
                    'yahoo_auction_end_time': item.yahoo_auction_end_time.isoformat(),
                }
                for item in ebay_register_items
            ]
            return create_success_response(response_data)
        except Exception as e:
            return create_error_response(str(e))