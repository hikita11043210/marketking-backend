"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import logging
from datetime import timedelta, datetime
from cryptography.fernet import Fernet
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# 開発環境の場合は.env.devを読み込む
if 'HEROKU' not in os.environ:
    env_path = BASE_DIR / '.env.dev'
    load_dotenv(env_path)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',') if os.getenv('ALLOWED_HOSTS') else []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'rest_framework',
    'corsheaders',
    'api',
    'rest_framework_simplejwt.token_blacklist',
    'social_django',  # Google認証用
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',  # Google認証用
                'social_django.context_processors.login_redirect',  # Google認証用
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'api.User'

# CORS設定
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True  # 開発環境のみ。本番環境では特定のオリジンのみを許可する
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    "x-ebay-token",
]
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',') if os.getenv('CORS_ALLOWED_ORIGINS') else [
    "http://localhost:3000",
    os.getenv('FRONTEND_URL'),
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '5/minute',
        'user': '100/minute',
        'admin': '1000/minute'  # 特定API用のカスタム制限追加
    }
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.google.GoogleOAuth2',  # Google認証用
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '{levelname} {asctime} {module} {message}',
#             'style': '{',
#         },
#     },
#     'handlers': {
#         'file': {
#             'level': 'ERROR',
#             'class': 'logging.FileHandler',
#             # 'filename': f'logs/debug_{datetime.now().strftime("%Y%m%d")}.log',
#             'formatter': 'verbose',
#         },
#         'console': {
#             'level': 'ERROR',
#             'class': 'logging.StreamHandler',
#             'formatter': 'verbose',
#         },
#     },
#     'loggers': {
#         '': {
#             'handlers': ['console', 'file'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#     },
# }

LOGGING = {
    'version': 1,  # 必須パラメータ
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        # その他のハンドラ...
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    # その他の設定...
}

# 環境変数
EBAY_OAUTH_SCOPES = os.getenv('EBAY_OAUTH_SCOPES', '').split(',')
EXCHANGE_RATE_API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')
EBAY_REDIRECT_URI = os.getenv('EBAY_REDIRECT_URI')
EBAY_IS_SANDBOX = os.getenv('EBAY_IS_SANDBOX', 'False').lower() == 'true'
EBAY_SANDBOX_URL = os.getenv('EBAY_SANDBOX_URL')
EBAY_SANDBOX_AUTH_URL = os.getenv('EBAY_SANDBOX_AUTH_URL')
EBAY_PRODUCTION_URL = os.getenv('EBAY_PRODUCTION_URL')
EBAY_PRODUCTION_AUTH_URL = os.getenv('EBAY_PRODUCTION_AUTH_URL')
EBAY_API_SITE_ID = os.getenv('EBAY_API_SITE_ID', '0')
DEEPL_API_URL = os.getenv('DEEPL_API_URL')
EBAY_MARKETPLACE_ID = os.getenv('EBAY_MARKETPLACE_ID')

# YahooAuction
YAHOO_AUCTION_URL = os.getenv('YAHOO_AUCTION_URL')
# JWT設定
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': os.getenv('JWT_SECRET_KEY', SECRET_KEY),
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

# Cookie設定
JWT_COOKIE_NAME = 'access_token'
JWT_REFRESH_COOKIE_NAME = 'refresh_token'
JWT_COOKIE_SECURE = True  # 本番環境ではTrue
JWT_COOKIE_SAMESITE = 'Strict'

# Google OAuth2 settings (将来の実装用)
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('GOOGLE_OAUTH2_KEY', '')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('GOOGLE_OAUTH2_SECRET', '')
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]

# 暗号化キーの設定
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')

# ebay送料
EBAY_SHIPPING_COST = os.getenv('EBAY_SHIPPING_COST')

# Payoneer手数料
PAYONEER_FEE = os.getenv('PAYONEER_FEE')

# Yahooフリーマーケット
YAHOO_FREE_MARKET_URL = os.getenv('YAHOO_FREE_MARKET_URL')
YAHOO_FREE_MARKET_ITEM_URL = os.getenv('YAHOO_FREE_MARKET_ITEM_URL')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')