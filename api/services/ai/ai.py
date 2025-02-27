from typing import List, Dict, Any
import openai
import json
import os
from dotenv import load_dotenv
import logging
from api.utils.generate_log_file import generate_log_file

# 環境変数の読み込み
load_dotenv()

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
            raise ValueError("タイトル、または商品詳細のキーが存在しません")

        # 動的なJSONフォーマットの生成
        json_format = json.dumps([{str(item): "xxxxx"} for item in category_aspects], ensure_ascii=False)
        items = ', '.join([str(item) for item in category_aspects])

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",  # または "gpt-4-turbo-preview"
                messages=[
                    {
                        "role": "system",
                        "content": """
                        あなたはカメラ、デジタルカメラ、レンズの専門家です。
                        製品タイトル、製品説明、必須項目、jsonフォーマットを元に、商品の詳細を抽出してください。

                        # 抽出ルール
                        - 情報は英語で返してください。
                        - もし情報が見つからない場合は 'None' を返してください。
                        - 結果は必ずJSONフォーマットの形式で返してください。
                        - 結果はすべてトップレベルでフラットに返してください。
                        - ネスト構造ではなく、各項目を独立して返してください。
                        - いかなる情報も1項目として、キーと値を返してください。
                        - 必須項目は必ずキーに含めてください。
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
                    {
                        "role": "user",
                        "content": f"jsonフォーマット: {json_format}"
                    }
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
                return json.loads(result_text)
            except json.JSONDecodeError:
                return [{item: None} for item in category_aspects]

        except Exception as e:
            raise Exception(f"商品情報の抽出中にエラーが発生しました: {str(e)}")
