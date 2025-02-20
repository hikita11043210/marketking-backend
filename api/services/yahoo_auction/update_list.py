from api.utils.response_helpers import create_success_response, create_error_response
from api.models.ebay import EbayRegisterFromYahooAuction
from api.services.ebay.item_status import ItemStatusService
from api.services.ebay.common import Common
from api.models.master import Status

class UpdateList(Common):
    def __init__(self, user):
        self.user = user

    def get(self):
        try:
            ebay_register_items = EbayRegisterFromYahooAuction.objects.all()
            
            for item in ebay_register_items:
                status = ItemStatusService(self.user).get_item_status(item.sku)
                if status == "ACTIVE":
                    item.status = Status.objects.get(id=1)
                elif status == "SOLD_OUT":
                    item.status = Status.objects.get(id=3)
                elif status == "ENDED":
                    item.status = Status.objects.get(id=2)
                elif status == "NOT_FOUND":
                    item.status = Status.objects.get(id=6)

                item.save()

            return create_success_response(ebay_register_items)
        except Exception as e:
            return create_error_response(str(e))