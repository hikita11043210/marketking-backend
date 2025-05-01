import os
import sys
import django
import logging

# パスの設定を修正
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

try:
    django.setup()
except ImportError as e:
    print(f"Django設定のインポートエラー: {e}")
    print(f"現在のパス: {sys.path}")
    sys.exit(1)

# ロギングの設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# カスタムUserモデルをインポート
from django.contrib.auth import get_user_model
User = get_user_model()  # プロジェクトのカスタムUserモデルを取得

from api.services.ebay.inventory import Inventory
from api.utils.generate import generate_merchant_location_key

def run_inventory_location_tools():
    """
    eBayのインベントリロケーション関連機能を簡易的に実行するツール
    """
    try:
        # ユーザーIDの入力
        user_id = int(input("ユーザーID（数字）を入力してください: ") or "34")
        
        # ユーザー取得
        try:
            user = User.objects.get(id=user_id)
            print(f"ユーザー: {user.username if hasattr(user, 'username') else user.email} (ID: {user.id})")
        except User.DoesNotExist:
            print(f"ID: {user_id} のユーザーが見つかりません。")
            return
        
        # インベントリサービスのインスタンスを作成
        inventory_service = Inventory(user)
        
        while True:
            print("\n実行する操作を選んでください:")
            print("1. ロケーション情報の一覧取得")
            print("2. 新しいロケーション情報の作成")
            print("0. 終了")
            
            choice = input("選択 (1, 2, 0): ").strip()
            
            if choice == "1":
                # ロケーション情報の取得
                print("\nロケーション情報を取得しています...")
                locations = inventory_service.get_inventory_locations()
                
                if locations and 'locations' in locations:
                    if locations['locations']:
                        print(f"\n取得したロケーション数: {len(locations['locations'])}")
                        for i, loc in enumerate(locations['locations'], 1):
                            print(f"\n==== ロケーション {i} ====")
                            print(f"merchantLocationKey: {loc.get('merchantLocationKey', 'N/A')}")
                            print(f"名称: {loc.get('name', 'N/A')}")
                            print(f"タイプ: {', '.join(loc.get('locationTypes', []))}")
                            
                            if 'location' in loc and 'address' in loc['location']:
                                addr = loc['location']['address']
                                print("住所:")
                                print(f"  {addr.get('addressLine1', '')}")
                                if 'addressLine2' in addr and addr['addressLine2']:
                                    print(f"  {addr['addressLine2']}")
                                print(f"  {addr.get('city', '')}, {addr.get('stateOrProvince', '')} {addr.get('postalCode', '')}")
                                print(f"  {addr.get('country', '')}")
                    else:
                        print("ロケーション情報が存在しません。")
                else:
                    print("ロケーション情報の取得に失敗しました。")
            
            elif choice == "2":
                # 新しいロケーション情報の作成
                print("\n新しいロケーション情報を作成します...")
                
                # 基本情報の入力
                name = input("ロケーション名 (例: 我が家): ") or "我が家"
                location_type = input("ロケーションタイプ (WAREHOUSE, STORE, FULFILLMENT_CENTER): ") or "WAREHOUSE"
                
                # 住所情報の入力
                print("\n住所情報を入力してください:")
                address_line1 = input("住所1 (例: 東明赤川): ") or "東明赤川"
                address_line2 = input("住所2 (例: 62-29): ") or "62-29"
                city = input("市区町村 (例: 四日市市): ") or "四日市市"
                state = input("都道府県 (例: 三重県): ") or "三重県"
                postal_code = input("郵便番号 (例: 5100805): ") or "5100805"
                country = input("国コード (例: JP): ") or "JP"
                phone = input("電話番号 (例: 0901234567): ") or "0901234567"
                
                # ロケーション情報の構築
                location_data = {
                    "location": {
                        "address": {
                            "addressLine1": address_line1,
                            "addressLine2": address_line2,
                            "city": city,
                            "stateOrProvince": state,
                            "postalCode": postal_code,
                            "country": country
                        }
                    },
                    "locationTypes": [location_type],
                    "name": name,
                    "merchantLocationStatus": "ENABLED",
                    "locationInstructions": "Created by test script",
                    "phone": phone
                }
                
                # 確認
                print("\n以下の情報でロケーションを作成します:")
                print(f"名称: {name}")
                print(f"タイプ: {location_type}")
                print(f"住所: {address_line1}, {address_line2}, {city}, {state}, {postal_code}, {country}")
                print(f"電話番号: {phone}")
                
                confirm = input("\n作成を続けますか？ (y/n): ").lower()
                if confirm == 'y':
                    try:
                        # マーチャントロケーションキーを生成
                        merchant_location_key = generate_merchant_location_key()
                        print(f"生成されたマーチャントロケーションキー: {merchant_location_key}")
                        
                        # ロケーション作成の実行
                        result = inventory_service.create_inventory_location(merchant_location_key, location_data)
                        print("\n作成結果:")
                        print(f"成功: {result.get('success', False)}")
                        print(f"メッセージ: {result.get('message', 'N/A')}")
                        
                        if 'data' in result and result['data']:
                            print("データ:", result['data'])
                    except Exception as e:
                        print(f"ロケーション作成中にエラーが発生しました: {str(e)}")
                else:
                    print("作成をキャンセルしました。")
            
            elif choice == "0":
                print("終了します。")
                break
            
            else:
                print("無効な選択です。もう一度試してください。")
    
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    run_inventory_location_tools() 