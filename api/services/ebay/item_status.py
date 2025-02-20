from api.services.ebay.inventory import Inventory
from api.services.ebay.offer import Offer
from api.services.ebay.common import Common

class ItemStatusService(Common):
    """eBayの商品状態を管理するサービスクラス"""
    
    def __init__(self, user):
        self.inventory_service = Inventory(user)
        self.offer_service = Offer(user)


    def get_item_status(self, sku: str):
        """
        商品の状態を総合的に判定する
        Returns:
            - ACTIVE: 出品中
            - SOLD_OUT: 売り切れ
            - ENDED: 取り下げ
            - NOT_FOUND: 商品が見つからない
        """
        try:
            # 在庫情報の取得
            inventory = self.inventory_service.get_inventory_item_for_sku(sku)
            if inventory is None:
                return None
            quantity = inventory.get('availability', {}).get('shipToLocationAvailability', {}).get('quantity', 0)
            
            # オファー状態の取得
            offer_status = self.offer_service.get_offer_status(sku)
            
            if offer_status == "PUBLISHED":
                if quantity > 0:
                    return "ACTIVE"  # 出品中で在庫あり
                else:
                    return "SOLD_OUT"  # 出品中だが在庫なし（売り切れ）
            else:
                return "ENDED"  # 取り下げ状態
                
        except Exception as e:
            raise Exception(f"商品状態の取得に失敗しました: {str(e)}")
