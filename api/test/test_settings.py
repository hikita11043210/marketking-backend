# 既存設定をインポートする前に環境変数を設定
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'

from project.settings import *

# データベース設定のみ上書き
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test_market_king',
        'USER': 'test_user',  # テスト用ユーザー名に変更
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
        'TEST': {
            'NAME': 'test_market_king',  # 明示的に指定
            'SERIALIZE': False
        }
    }
}

# テスト用設定を追加
DEBUG = True