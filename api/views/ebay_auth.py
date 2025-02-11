from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.services.ebay_auth import EbayAuthService
from api.models import EbayToken
from datetime import datetime

class EbayAuthStatusView(APIView):
    """eBayとの連携状態を確認するAPI"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = EbayToken.objects.filter(user=request.user).first()
        return Response({
            'is_connected': bool(token),
            'expires_at': token.expires_at.isoformat() if token else None
        })

class EbayAuthURLView(APIView):
    """eBay認証用URLを取得するAPI"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        service = EbayAuthService(request.user)
        return Response({
            'url': service.get_auth_url()
        })

class EbayAuthCallbackView(APIView):
    """eBay認証コールバック処理API"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response(
                {'error': 'Authorization code is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        service = EbayAuthService(request.user)
        try:
            token = service.exchange_code_for_token(code, request.user.id)
            return Response({
                'message': 'Successfully connected to eBay',
                'expires_at': token.expires_at.isoformat()
            })
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class EbayAuthDisconnectView(APIView):
    """eBayとの連携を解除するAPI"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        EbayToken.objects.filter(user=request.user).delete()
        return Response({
            'message': 'Successfully disconnected from eBay'
        }) 