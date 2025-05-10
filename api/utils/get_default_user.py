from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

def get_default_user():
    """デフォルトユーザー（anakin0719）を取得する共通処理"""
    try:
        return User.objects.get(username='anakin0719')
    except User.DoesNotExist:
        logger.error("デフォルトユーザー（anakin0719）が見つかりません")
        raise 