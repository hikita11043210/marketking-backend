from api.utils.response_helpers import create_success_response, create_error_response
from api.models.ebay import Ebay
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
            updated_items = []
            total_items = 0
            
            with transaction.atomic():
                ebay_register_items = Ebay.objects.select_for_update().filter(status_id=1)
                total_items = ebay_register_items.count()
                
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
                            new_status = StatusModel.objects.get(id=5)
                        
                        if new_status and item.status.id != new_status.id:
                            old_status_id = item.status.id
                            item.status = new_status
                            item.save()
                            logger.info(f"ステータスを更新しました - SKU: {item.sku}, 新しいステータス: {new_status.id}")
                            
                            # 更新情報を記録
                            updated_items.append({
                                'sku': item.sku,
                                'old_status': old_status_id,
                                'new_status': new_status.id
                            })
                    
                    except Exception as item_error:
                        logger.error(f"商品の同期中にエラーが発生しました - SKU: {item.sku}, エラー: {str(item_error)}")
                        continue

            return {
                'total_items': total_items,
                'updated_count': len(updated_items),
                'updated_items': updated_items
            }
            
        except Exception as e:
            logger.error(f"ステータスの同期処理でエラーが発生しました: {str(e)}")
            return str(e)