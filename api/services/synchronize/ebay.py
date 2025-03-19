from api.utils.response_helpers import create_success_response, create_error_response
from api.models.ebay import Ebay
from api.services.ebay.item_status import ItemStatusService
from api.models.master import Status as StatusModel
from django.db import transaction
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class Status():
    def __init__(self, user):
        self.user = user

    def synchronize(self):
        try:
            synchronize_start_time = timezone.now()
            updated_items = []
            total_items = 0
            count_active_items = 0
            count_sold_out_items = 0
            count_change_status_items = 0
            
            with transaction.atomic():
                ebay_register_items = (
                    Ebay.objects
                    .select_for_update()
                    .filter(status_id=1)
                )
                
                ebay_register_items = ebay_register_items.select_related('status')
                total_items = ebay_register_items.count()
                
                for item in ebay_register_items:
                    try:
                        status = ItemStatusService(self.user).get_item_status(item.sku)
                        
                        new_status = None
                        if status == "ACTIVE":
                            new_status = StatusModel.objects.get(id=1)
                        elif status == "SOLD_OUT":
                            new_status = StatusModel.objects.get(id=3)
                        elif status == "ENDED":
                            new_status = StatusModel.objects.get(id=2)
                        elif status == "NOT_FOUND":
                            new_status = StatusModel.objects.get(id=5)
                        
                        if new_status:
                            if item.status.id != new_status.id:
                                old_status_id = item.status.id
                                item.status = new_status
                                item.save()
                                
                                updated_items.append({
                                    'sku': item.sku,
                                    'old_status': old_status_id,
                                    'new_status': new_status.id
                                })
                                
                                if old_status_id == 1:
                                    count_change_status_items += 1
                            
                            if new_status.id == 1:
                                count_active_items += 1
                            elif new_status.id == 3:
                                count_sold_out_items += 1
                    
                    except Exception as item_error:
                        logger.error(f"商品の同期中にエラーが発生しました - SKU: {item.sku}, エラー: {str(item_error)}")
                        continue

                synchronize_end_time = timezone.now()

                return {
                    'synchronize_start_time': synchronize_start_time,
                    'synchronize_end_time': synchronize_end_time,
                    'synchronize_target_item': total_items,
                    'count_active_item': count_active_items,
                    'count_sold_out_item': count_sold_out_items,
                    'count_change_status_item': count_change_status_items,
                    'updated_count': len(updated_items),
                    'updated_items': updated_items
                }
                
        except Exception as e:
            logger.error(f"ステータスの同期処理でエラーが発生しました: {str(e)}")
            return str(e)