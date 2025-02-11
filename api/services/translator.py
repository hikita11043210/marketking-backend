import logging
import requests
from django.conf import settings
from typing import Dict, Optional
from ..models.master import Setting

logger = logging.getLogger(__name__)

class TranslatorService:
    def __init__(self, user):
        self.user = user
        self.auth_key = Setting.get_settings(user).deepl_api_key
        self.DEEPL_API_URL = settings.DEEPL_API_URL

    def translate_text(self, text: str, target_lang: str = 'EN') -> Dict:
        """
        テキストを翻訳する

        Args:
            text (str): 翻訳対象のテキスト
            target_lang (str): 翻訳先の言語コード（デフォルト: 'EN'）

        Returns:
            Dict: 翻訳結果
                - translated_text: 翻訳されたテキスト
                - source_lang: 検出された元の言語
                - target_lang: 翻訳先の言語

        Raises:
            ValueError: パラメータが不正な場合
            Exception: API呼び出しに失敗した場合
        """
        try:
            if not text:
                raise ValueError("翻訳するテキストが指定されていません。")

            headers = {
                'Authorization': f'DeepL-Auth-Key {self.auth_key}',
                'Content-Type': 'application/json'
            }

            data = {
                'text': [text],
                'target_lang': target_lang
            }

            response = requests.post(self.DEEPL_API_URL, headers=headers, json=data)
            response.raise_for_status()

            result = response.json()
            translation = result['translations'][0]

            return {
                'translated_text': translation['text'],
                'source_lang': translation['detected_source_language'],
                'target_lang': target_lang
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"DeepL API呼び出しエラー: {str(e)}")
            if response.status_code == 429:
                raise Exception("API使用制限に達しました。しばらく待ってから再試行してください。")
            elif response.status_code == 456:
                raise Exception("文字数制限を超えています。")
            else:
                raise Exception("翻訳APIでエラーが発生しました。")

        except Exception as e:
            logger.error(f"翻訳エラー: {str(e)}")
            raise 