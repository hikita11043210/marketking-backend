from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.settings import api_settings
from rest_framework import authentication

class AsyncJWTAuthentication(authentication.BaseAuthentication):
    def get_header(self, request):
        header = request.META.get('HTTP_AUTHORIZATION')
        if not header:
            return None
        return header

    def get_raw_token(self, header):
        parts = header.split()
        if len(parts) == 0:
            return None

        if parts[0] not in ('Bearer',):
            return None

        if len(parts) != 2:
            return None

        return parts[1]

    async def authenticate(self, request):
        try:
            header = self.get_header(request)
            if header is None:
                return None

            raw_token = self.get_raw_token(header)
            if raw_token is None:
                return None

            validated_token = await sync_to_async(self.get_validated_token)(raw_token)
            user = await self.get_user_async(validated_token)
            return (user, validated_token)
        except Exception as e:
            return None

    @sync_to_async
    def get_validated_token(self, raw_token):
        """
        非同期でトークンを検証
        """
        try:
            return JWTAuthentication().get_validated_token(raw_token)
        except TokenError as e:
            raise InvalidToken(e.args[0])

    @sync_to_async
    def get_user_async(self, validated_token):
        """
        非同期でユーザーを取得
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
            user = get_user_model().objects.get(**{api_settings.USER_ID_FIELD: user_id})

            if not user.is_active:
                raise InvalidToken('User is inactive')

            return user
        except (KeyError, get_user_model().DoesNotExist):
            raise InvalidToken('Token contained no recognizable user identification') 