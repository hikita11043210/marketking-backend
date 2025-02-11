from cryptography.fernet import Fernet
from django.conf import settings

def get_encryption_key():
    """暗号化キーを取得します"""
    return settings.ENCRYPTION_KEY

def encrypt_value(value: str) -> str:
    """文字列を暗号化します"""
    if not value:
        return value
    f = Fernet(get_encryption_key())
    return f.encrypt(value.encode()).decode()

def decrypt_value(encrypted_value: str) -> str:
    """暗号化された文字列を復号化します"""
    if not encrypted_value:
        return encrypted_value
    f = Fernet(get_encryption_key())
    return f.decrypt(encrypted_value.encode()).decode() 