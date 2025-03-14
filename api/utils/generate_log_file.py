import json
import os
from datetime import datetime

def generate_log_file(data, path, date=False):
    """ログファイルを生成する"""
    # ディレクトリが存在しない場合は作成
    os.makedirs(os.path.dirname(f'logs/{path}'), exist_ok=True)
    
    # 現在時刻を取得
    current_time = datetime.now()
    
    # ファイル名の生成
    filename = f"{'_' + current_time.strftime('%Y%m%d') if date else ''}.json"
    filepath = f"logs/{path}{filename}"
    
    # 既存のログデータを読み込む
    existing_data = []
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                if not isinstance(existing_data, list):
                    existing_data = [existing_data]
        except json.JSONDecodeError:
            existing_data = []
    
    # 新しいログデータを追加
    timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
    log_entry = {
        'timestamp': timestamp,
        'data': data
    }
    existing_data.append(log_entry)
    
    # JSONファイルの書き込み
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)
