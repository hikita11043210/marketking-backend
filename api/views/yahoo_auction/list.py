from rest_framework.views import APIView
from api.utils.response_helpers import create_success_response, create_error_response
from api.models.ebay import Ebay
from api.services.currency import CurrencyService
from decimal import Decimal
from api.services.ebay.offer import Offer
from api.utils.generate_log_file import generate_log_file
from api.services.ebay.inventory import Inventory
from api.services.synchronize.ebay import Status
from api.services.synchronize.yahoo_auction import SynchronizeYahooAuction

class ListView(APIView):
    def get(self, request):
        try:
            # 商品情報を取得（YahooAuctionとの関連を含める）
            ebay_register_items = Ebay.objects.select_related(
                'yahoo_auction_id',
                'yahoo_auction_id__status',
                'status'
            ).filter(yahoo_auction_id__isnull=False).order_by('status', '-update_datetime')
            
            # # 出品情報を削除するためのインスタンスを生成
            # ebay_service_offer = Offer(request.user)
            # ebay_service_inventory = Inventory(request.user)
            # data = ebay_service_inventory.get_inventory_items()
            # generate_log_file(data, "data", date=False)
            # ebay_service_inventory.delete_inventory_item('YA_e1163351978_20250222024545')
            # # 出品情報を削除
            # for item in data:
            #     ebay_service_inventory.delete_inventory_item(item['sku']) # ebayから削除

            # 一覧出力時の変換レートを取得
            rate = Decimal(str(CurrencyService.get_exchange_rate('USD', 'JPY')))

            # 一覧出力時のデータを作成
            response_data = [
                {
                    'id': item.id,
                    'status': item.status.status_name,
                    'sku': item.sku,
                    'offer_id': item.offer_id,
                    'ebay_price': int(item.price * rate),  # priceに変更
                    'ebay_shipping_price': int(item.shipping_price),  # shipping_priceに変更
                    'final_profit': int(item.final_profit * rate),
                    'yahoo_auction_id': item.yahoo_auction_id.unique_id,  # unique_idを参照
                    'yahoo_auction_url': item.yahoo_auction_id.url,
                    'yahoo_auction_item_name': item.yahoo_auction_id.item_name,
                    'yahoo_auction_item_price': str(item.yahoo_auction_id.item_price),
                    'yahoo_auction_shipping': str(item.yahoo_auction_id.shipping),
                    'purchase_price': int(item.yahoo_auction_id.item_price + item.yahoo_auction_id.shipping),
                    'yahoo_auction_end_time': item.yahoo_auction_id.end_time.isoformat(),
                    'yahoo_auction_status': item.yahoo_auction_id.status.status_name,
                    'update_datetime': item.update_datetime
                }
                for item in ebay_register_items
            ]
            
            # ステータスごとの商品数を追加
            response_data = {
                'items': response_data,
                'counts': {
                    'active': ebay_register_items.filter(status_id=1).count(),
                    'sold_out': ebay_register_items.filter(status_id=2).count(),
                }
            }
            return create_success_response(response_data)
        except Exception as e:
            return create_error_response(str(e))

class SynchronizeYahooAuctionView(APIView):
    def get(self, request):
        try:
            response = SynchronizeYahooAuction(request.user).synchronize()
            return create_success_response(data=response,message="Yahooオークションの同期が完了しました")
        except Exception as e:
            return create_error_response(str(e))