from api.utils.response_helpers import create_success_response, create_error_response
from api.models.ebay import EbayRegisterFromYahooAuction
from api.services.ebay.item_status import ItemStatusService
from api.models.master import Status as StatusModel
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

class Status():
    def __init__(self, user):
        self.user = user

    def synchronize(self):
        """
        eBayの商品ステータスを同期する
        """
        try:
            with transaction.atomic():
                ebay_register_items = EbayRegisterFromYahooAuction.objects.select_for_update().all()
                
                for item in ebay_register_items:
                    try:
                        status = ItemStatusService(self.user).get_item_status(item.sku)
                        logger.info(f"SKU: {item.sku}, 現在のステータス: {item.status.id}, 新しいステータス: {status}")
                        
                        new_status = None
                        if status == "ACTIVE":
                            new_status = StatusModel.objects.get(id=1)
                        elif status == "SOLD_OUT":
                            new_status = StatusModel.objects.get(id=3)
                        elif status == "ENDED":
                            new_status = StatusModel.objects.get(id=2)
                        elif status == "NOT_FOUND":
                            new_status = StatusModel.objects.get(id=6)
                        
                        if new_status and item.status.id != new_status.id:
                            item.status = new_status
                            item.save()
                            logger.info(f"ステータスを更新しました - SKU: {item.sku}, 新しいステータス: {new_status.id}")
                    
                    except Exception as item_error:
                        logger.error(f"商品の同期中にエラーが発生しました - SKU: {item.sku}, エラー: {str(item_error)}")
                        continue

            return create_success_response("ステータスの同期が完了しました")
            
        except Exception as e:
            logger.error(f"ステータス同期処理でエラーが発生しました: {str(e)}")
            return create_error_response("ステータスの同期に失敗しました")