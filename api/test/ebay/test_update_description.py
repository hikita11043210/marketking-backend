import os
import sys
import django
from pathlib import Path

# プロジェクトのルートディレクトリをPYTHONPATHに追加
project_root = str(Path(__file__).resolve().parent.parent.parent.parent)
sys.path.append(project_root)

# Django設定を読み込む
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

# 必要なモジュールをインポート
from django.contrib.auth import get_user_model
from api.services.ebay.trading import Trading

User = get_user_model()

def test_update_description():
    """
    Trading.update_item_descriptionメソッドを直接テストする
    """
    try:
        # テスト用のユーザーを取得（実際の存在するユーザーのユーザー名に変更してください）
        user = User.objects.get(username='anakin0512')
        
        # テスト用の商品ID
        ebay_item_id = '205452963255'  # テスト用のeBay商品ID（実際に存在するIDに変更してください）
        
        # テスト用の商品説明
        description = "aaaa"
        
        # Tradingサービスのインスタンスを作成
        trading_service = Trading(user)
        
        # 商品説明を更新
        result = trading_service.update_item_description(ebay_item_id, description)
        
        # 結果を表示
        print("テスト結果:")
        print(f"成功: {result.get('success', False)}")
        print(f"メッセージ: {result.get('message', '')}")
        print(f"データ: {result.get('data', {})}")
        
        return result
        
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        raise

if __name__ == "__main__":
    # テスト実行
    test_update_description() 