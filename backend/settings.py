# Async Settings
ASGI_APPLICATION = 'backend.asgi.application'

# JWT Settings for Async
SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

# 開発環境でのみ有効にする
if DEBUG:
    DJANGO_ALLOW_ASYNC_UNSAFE = True

# タイムアウト設定
ASYNC_TIMEOUT = 300  # 5分 