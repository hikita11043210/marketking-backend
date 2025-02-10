from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from django.contrib.auth import authenticate
from django.conf import settings
from django.middleware import csrf
from datetime import datetime

class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({
                'error': 'unauthorized',
                'message': 'ユーザー名またはパスワードが正しくありません'
            }, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = Response({
            'accessToken': access_token,
            'refreshToken': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        })

        # CSRFトークンを設定
        csrf.get_token(request)

        # Cookieの設定
        response.set_cookie(
            settings.JWT_COOKIE_NAME,
            access_token,
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
            httponly=True,
            samesite=settings.JWT_COOKIE_SAMESITE,
            secure=settings.JWT_COOKIE_SECURE
        )
        response.set_cookie(
            settings.JWT_REFRESH_COOKIE_NAME,
            str(refresh),
            max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
            httponly=True,
            samesite=settings.JWT_COOKIE_SAMESITE,
            secure=settings.JWT_COOKIE_SECURE
        )

        return response

class RefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh_token')
        
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            response = Response({
                'accessToken': access_token
            })

            # 新しいアクセストークンをCookieに設定
            response.set_cookie(
                settings.JWT_COOKIE_NAME,
                access_token,
                max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
                httponly=True,
                samesite=settings.JWT_COOKIE_SAMESITE,
                secure=settings.JWT_COOKIE_SECURE
            )

            return response

        except TokenError:
            return Response({
                'error': 'unauthorized',
                'message': '無効なトークンです'
            }, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refreshToken')
            token = RefreshToken(refresh_token)
            
            # トークンをブラックリストに追加
            token.blacklist()

            response = Response({
                'message': 'ログアウトしました'
            })

            # Cookieを削除
            response.delete_cookie(settings.JWT_COOKIE_NAME)
            response.delete_cookie(settings.JWT_REFRESH_COOKIE_NAME)

            return response

        except TokenError:
            return Response({
                'error': 'unauthorized',
                'message': '無効なトークンです'
            }, status=status.HTTP_401_UNAUTHORIZED) 