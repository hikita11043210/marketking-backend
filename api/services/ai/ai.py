from typing import List, Dict, Any
import openai
import json
import os
from dotenv import load_dotenv
import logging
from api.utils.generate_log_file import generate_log_file

# 環境変数の読み込み
load_dotenv(override=True)

class Ai:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def extract_cameras_specifics(self, title: str, category_aspects: List[str], description: str) -> Dict[str, Any]:
        """
        商品タイトルから特定の情報を抽出するサービス
        
        Args:
            title: 商品タイトル
            category_aspects: 抽出したい項目のリスト
            
        Returns:
            Dict[str, Any]: 抽出された商品情報
            
        Raises:
            ValueError: タイトルまたは項目リストが無効な場合
        """
        if not title or not category_aspects:
            return ""

        # 動的なJSONフォーマットの生成
        items = ', '.join([str(item) for item in category_aspects])

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",  # または "gpt-4-turbo-preview"
                messages=[
                    {
                        "role": "system",
                        "content": """
                        製品タイトル、製品説明を元に、商品の詳細を抽出してください。
                        製品タイトル、製品説明以外からもあなたが持つ知識を元に、商品の詳細を抽出してください。

                        # 抽出ルール
                        - 情報は英語で返してください。
                        - 必ず出力フォーマットに従ってください。
                        - 製品に関するスペックのみを抽出してください。
                        - 必須項目は必ずキーに含めてください。
                        - 結果はすべてトップレベルでフラットに返してください。
                        - ネスト構造ではなく、各項目を独立して返してください。
                        - いかなる情報も1項目として、キーと値を返してください。

                        # 出力フォーマット
                        {
                            "key1": "value1",
                            "key2": "value2",
                            "key3": "value3"
                        }
                        """
                    },
                    {
                        "role": "user",
                        "content": f"製品タイトル: {title}"
                    },
                    {
                        "role": "user",
                        "content": f"製品説明: {description}"
                    },
                    {
                        "role": "user",
                        "content": f"必須項目: {items}"
                    },
                ],
                temperature=0.0  # より適切な回答を得るためにtemperatureを追加
            )

            # 使用量情報をログに記録
            total_tokens = response.usage.total_tokens
            max_tokens = 4096 if response.model == "gpt-3.5-turbo" else 128000  # GPT-4の場合

            log_data = {
                'モデル': response.model,
                'トークン使用状況': {
                    'プロンプトトークン数': response.usage.prompt_tokens,
                    '応答トークン数': response.usage.completion_tokens,
                    '合計トークン数': total_tokens,
                    '使用率': f"{(total_tokens / max_tokens * 100):.2f}%",
                    '残りトークン数': max_tokens - total_tokens
                },
                '応答時間': {
                    '作成日時': response.created,
                    '処理時間': f"{response.response_ms / 1000:.2f}秒" if hasattr(response, 'response_ms') else "不明"
                },
                'モデル設定': {
                    '温度設定': 0.0,
                    'モデルバージョン': response.model
                },
                '応答内容': response.choices[0].message.content,
                '応答状態': {
                    '終了理由': response.choices[0].finish_reason,
                    '応答インデックス': response.choices[0].index
                }
            }

            generate_log_file(log_data, "extract_specifics", date=True)

            result_text = response.choices[0].message.content
            
            try:
                # JSONとしてパース
                parsed_result = json.loads(result_text)
                
                # 必ず保持するキーのリスト（空でも削除しないキー）
                required_keys = category_aspects  # category_aspectsは必須項目のリスト
                
                # 配列形式かどうかをチェック
                if isinstance(parsed_result, list) and all(isinstance(item, dict) and len(item) == 1 for item in parsed_result):
                    # 配列形式から辞書形式に変換
                    converted_result = {}
                    for item in parsed_result:
                        for key, value in item.items():
                            # 必須キーか、空でない値を持つキーを追加
                            if key in required_keys or value not in [None, "", [], {}, "None"]:
                                converted_result[key] = value
                    
                    # 必須キーが結果に含まれていない場合は追加（Noneとして）
                    for key in required_keys:
                        if key not in converted_result:
                            converted_result[key] = None
                            
                    return converted_result
                elif isinstance(parsed_result, dict):
                    # 辞書形式の場合は必須キー以外の空の値を持つキーを削除
                    result = {k: v for k, v in parsed_result.items() 
                             if k in required_keys or v not in [None, "", [], {}, "None"]}
                    
                    # 必須キーが結果に含まれていない場合は追加（Noneとして）
                    for key in required_keys:
                        if key not in result:
                            result[key] = None
                            
                    return result
                else:
                    # 想定外の形式の場合はそのまま返す
                    return parsed_result
            except json.JSONDecodeError:
                return {item: None for item in category_aspects}

        except Exception as e:
            raise Exception(f"商品情報の抽出中にエラーが発生しました: {str(e)}")

    def get_category_id(self, categories: List[Dict[str, Any]], title: str) -> str:
        """
        商品タイトルに基づいて最適なカテゴリIDを選択する
        
        Args:
            categories: カテゴリ情報のリスト
            title: 商品タイトル
            
        Returns:
            str: 選択されたカテゴリID
            
        Raises:
            ValueError: カテゴリリストが空または無効な場合
        """
        if not categories or not isinstance(categories, list):
            raise ValueError("カテゴリリストが無効です")
        
        if not title:
            raise ValueError("商品タイトルが無効です")
        
        try:
            # カテゴリ情報を整形
            category_info = []
            for category in categories:
                category_info.append({
                    "id": category.get("categoryId", ""),
                    "name": category.get("categoryName", ""),
                    "path": category.get("path", "")
                })
            
            # OpenAI APIを使用して最適なカテゴリを選択
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """
                        あなたは商品カテゴリ分類の専門家です。
                        商品タイトルを分析し、提供されたカテゴリリストから最も適切なカテゴリを選択してください。
                        
                        # 選択ルール
                        - 商品タイトルの内容と最も関連性の高いカテゴリを選んでください
                        - カメラ、レンズ、アクセサリーなどの特徴を考慮してください
                        - 結果は必ずカテゴリIDのみを返してください（数字のみ）
                        - 説明や理由は不要です
                        """
                    },
                    {
                        "role": "user",
                        "content": f"商品タイトル: {title}\nカテゴリリスト: {json.dumps(category_info, ensure_ascii=False)}"
                    }
                ],
                temperature=0.0
            )
            
            # 使用量情報をログに記録
            total_tokens = response.usage.total_tokens
            max_tokens = 4096 if response.model == "gpt-3.5-turbo" else 128000
            
            log_data = {
                'モデル': response.model,
                'トークン使用状況': {
                    'プロンプトトークン数': response.usage.prompt_tokens,
                    '応答トークン数': response.usage.completion_tokens,
                    '合計トークン数': total_tokens,
                    '使用率': f"{(total_tokens / max_tokens * 100):.2f}%",
                    '残りトークン数': max_tokens - total_tokens
                },
                '応答内容': response.choices[0].message.content,
                '応答状態': {
                    '終了理由': response.choices[0].finish_reason
                }
            }
            
            generate_log_file(log_data, "get_category_id", date=True)
            
            # 応答からカテゴリIDを抽出
            category_id = response.choices[0].message.content.strip()
            
            # 数字のみであることを確認
            if not category_id.isdigit():
                # 数字以外の文字が含まれている場合は、数字部分のみを抽出
                import re
                digits = re.findall(r'\d+', category_id)
                if digits:
                    category_id = digits[0]
                else:
                    # デフォルトとして最初のカテゴリを使用
                    category_id = categories[0].get("categoryId", "")
            
            # 選択されたカテゴリIDが実際にリスト内に存在するか確認
            valid_ids = [cat.get("categoryId", "") for cat in categories]
            if category_id not in valid_ids:
                # 存在しない場合は最初のカテゴリを使用
                category_id = categories[0].get("categoryId", "")
            
            return category_id
            
        except Exception as e:
            # エラーが発生した場合はログに記録し、最初のカテゴリを返す
            generate_log_file(f"カテゴリID選択中にエラーが発生しました: {str(e)}", "get_category_id_error", date=True)
            return categories[0].get("categoryId", "")