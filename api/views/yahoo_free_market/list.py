from rest_framework.views import APIView
from api.utils.response_helpers import create_success_response, create_error_response
from api.models.ebay import Ebay
from api.services.currency import CurrencyService
from decimal import Decimal
from api.services.ebay.offer import Offer
from api.utils.generate_log_file import generate_log_file
from api.services.ebay.inventory import Inventory
from api.services.synchronize.ebay import Status
from api.services.synchronize.yahoo_free_market import SynchronizeYahooFreeMarket

class YahooFreeMarketListView(APIView):
    def get(self, request):
        try:
            # パラメータを取得
            search = request.query_params.get('search')
            limit = request.query_params.get('limit')
            page = request.query_params.get('page')

            # 商品情報を取得（YahooAuctionとの関連を含める）
            list_items = Ebay.objects.select_related(
                'yahoo_free_market_id',
                'yahoo_free_market_id__status',
                'status'
            ).filter(yahoo_free_market_id__isnull=False)
            
            # # 出品情報を削除するためのインスタンスを生成
            # ebay_service_offer = Offer(request.user)
            # ebay_service_inventory = Inventory(request.user)
            # data = ebay_service_inventory.get_inventory_items()
            # generate_log_file(data, "data", date=False)
            # ebay_service_inventory.delete_inventory_item('YA_e1163351978_20250222024545')
            # # 出品情報を削除
            # for item in data:
            #     print(item['sku'])
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
                    'yahoo_free_market_id': item.yahoo_free_market_id.unique_id,  # unique_idを参照
                    'yahoo_free_market_url': item.yahoo_free_market_id.url,
                    'yahoo_free_market_item_name': item.yahoo_free_market_id.item_name,
                    'yahoo_free_market_item_price': str(item.yahoo_free_market_id.item_price),
                    'yahoo_free_market_shipping': str(item.yahoo_free_market_id.shipping),
                    'purchase_price': int(item.yahoo_free_market_id.item_price + item.yahoo_free_market_id.shipping),
                    'yahoo_free_market_status': item.yahoo_free_market_id.status.status_name
                }
                for item in list_items
            ]
            return create_success_response(response_data)
        except Exception as e:
            return create_error_response(str(e))


class SynchronizeYahooFreeMarketView(APIView):
    def get(self, request):
        try:
            response = SynchronizeYahooFreeMarket(request.user).synchronize()
            return create_success_response(data=response,message="Yahooフリーマーケットの同期が完了しました")
        except Exception as e:
            return create_error_response(str(e))