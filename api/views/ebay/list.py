from api.services.yahoo_auction.update_list import UpdateList
from rest_framework.views import APIView
from api.services.ebay.inventory import Inventory
from api.utils.response_helpers import create_success_response, create_error_response
from api.models.ebay import EbayRegisterFromYahooAuction
from api.services.ebay.offer import Offer
from api.utils.generate_log_file import generate_log_file
from api.services.currency import CurrencyService
from decimal import Decimal
from datetime import datetime

class List(APIView):
    def get(self, request):
        try:
            # ebay_service_inventory = Inventory(request.user)
            # ebay_service_offer = Offer(request.user)
            # inventory_items = ebay_service_inventory.get_inventory_items()

            # generate_log_file(inventory_items, "inventory_items", time=False)

            ebay_register_items = EbayRegisterFromYahooAuction.objects.all()
            
            # for item in ebay_register_items:
            #     offer = ebay_service_offer.get_offer_status(item.sku)
            #     ebay_service_offer.publish_offer(offer.get('offerId'))

            # offer = ebay_service_offer.get_offer_status('YA_q1173962949_20250220234441')
            # ebay_service_offer.publish_offer(offer.get('offerId'))
            # generate_log_file(offer, "offer", time=False)
            rate = Decimal(str(CurrencyService.get_exchange_rate('USD', 'JPY')))
            response_data = [
                {
                    'id': item.id,
                    'status': item.status.status_name,
                    'sku': item.sku,
                    'ebay_price': int(item.ebay_price * rate),
                    'ebay_shipping_price': int(item.ebay_shipping_price * rate),
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