import logging
import requests
from django.conf import settings
from typing import Dict, Optional
from ..models.master import Setting
import deepl

logger = logging.getLogger(__name__)

class TranslatorService:
    def __init__(self, user):
        self.user = user
        self.auth_key = Setting.get_settings(user).deepl_api_key
        self.DEEPL_API_URL = settings.DEEPL_API_URL

    def translate_text(self, text: str, target_lang: str) -> Dict:
        """
        テキストを翻訳する
        Args:
            text (str): 翻訳対象のテキスト
            target_lang (str): 翻訳先の言語コード（デフォルト: 'EN-US'）

        Returns:
            Dict: 翻訳結果
                - translated_text: 翻訳されたテキスト
        """
        try:
            if not self.auth_key:
                raise Exception("DeepL APIキーが設定されていません。")
            translator = deepl.Translator(self.auth_key)
            result = translator.translate_text(text, target_lang=target_lang)
            return {
                'translated_text': result.text,
                'target_lang': target_lang
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"DeepL API呼び出しエラー: {str(e)}")
            if result.status_code == 429:
                raise Exception("API使用制限に達しました。しばらく待ってから再試行してください。")
            elif result.status_code == 456:
                raise Exception("文字数制限を超えています。")
            else:
                raise Exception("翻訳APIでエラーが発生しました。")

        except Exception as e:
            logger.error(f"翻訳エラー: {str(e)}")
            raise 