from api.utils.response_helpers import create_success_response, create_error_response
from api.models.ebay import EbayRegisterFromYahooAuction
from api.services.ebay.item_status import ItemStatusService
from api.services.ebay.common import Common

class UpdateList(Common):
    def __init__(self, user):
        self.user = user

    def get(self):
        try:
            ebay_register_items = EbayRegisterFromYahooAuction.objects.all()
            
            for item in ebay_register_items:
                status = ItemStatusService(self.user).get_item_status(item.sku)

                if status == "ACTIVE":
                    print("出品中")
                elif status == "SOLD_OUT":
                    print("売り切れ")
                elif status == "ENDED":
                    print("取り下げ")

            return create_success_response(ebay_register_items)
        except Exception as e:
            return create_error_response(str(e))