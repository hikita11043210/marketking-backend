from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

def get_default_user():
    """デフォルトユーザー（anakin0512）を取得する共通処理"""
    try:
        return User.objects.get(username='anakin0512')
    except User.DoesNotExist:
        logger.error("デフォルトユーザー（anakin0512）が見つかりません")
        raise 