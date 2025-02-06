from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from ..services.ebay_auth import EbayAuthService
from ..services.ebay_inventory import EbayInventoryService
from ..services.ebay_categories import EbayCategoriesService
from ..services.ebay_policies import EbayPoliciesService
import logging
from rest_framework.decorators import api_view
from ebaysdk.trading import Connection as Trading
from django.conf import settings
import json
from ..models import Setting
from django.utils import timezone
import requests
from base64 import b64encode

logger = logging.getLogger(__name__)

class EbayAuthView(APIView):
    def get(self, request):
        """認可URLを取得"""
        try:
            auth_service = EbayAuthService()
            state = request.GET.get('state', '')
            auth_url = auth_service.get_authorization_url(state)
            
            return Response({
                'success': True,
                'data': {
                    'auth_url': auth_url
                }
            })
            
        except Exception as e:
            logger.error(f"Failed to get authorization URL: {str(e)}")
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """認可コードをトークンと交換"""
        try:
            auth_service = EbayAuthService()
            code = request.data.get('code')
            if not code:
                raise ValidationError("認可コードが必要です")
                
            tokens = auth_service.exchange_code_for_tokens(code)
            
            return Response({
                'success': True,
                'data': tokens
            })
            
        except Exception as e:
            logger.error(f"Failed to exchange code for tokens: {str(e)}")
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class EbayRegisterView(APIView):
    def post(self, request):
        """商品をeBayに登録"""
        try:
            inventory_service = EbayInventoryService(user_id=request.user.id)
            offer_id = inventory_service.create_inventory_item(request.data)
            
            return Response({
                'success': True,
                'message': '商品を登録しました',
                'data': {'offer_id': offer_id}
            })
            
        except Exception as e:
            logger.error(f"Failed to register product: {str(e)}")
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class EbayCategoriesView(APIView):
    def get(self, request):
        """カテゴリー情報を取得"""
        try:
            categories_service = EbayCategoriesService(user_id=request.user.id)
            marketplace_id = request.GET.get('marketplace_id', 'EBAY_US')
            category_tree = categories_service.get_category_tree(marketplace_id=marketplace_id)
            
            return Response({
                'success': True,
                'data': category_tree
            })
            
        except Exception as e:
            logger.error(f"Failed to get categories: {str(e)}")
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """カテゴリーを検索"""
        try:
            categories_service = EbayCategoriesService(user_id=request.user.id)
            query = request.data.get('query')
            marketplace_id = request.data.get('marketplace_id', 'EBAY_US')
            
            if not query:
                raise ValidationError("検索クエリが必要です")
                
            suggestions = categories_service.get_category_suggestions(query, marketplace_id)
            
            return Response({
                'success': True,
                'data': suggestions
            })
            
        except Exception as e:
            logger.error(f"Failed to search categories: {str(e)}")
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class EbayPoliciesView(APIView):
    def get(self, request):
        """ポリシー情報を取得"""
        try:
            token = request.GET.get('token')
            marketplace_id = request.GET.get('marketplace_id', 'EBAY_US')

            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            # eBay Account APIのベースURL
            base_url = 'https://api.ebay.com/sell/account/v1'
            #base_url = 'https://api.sandbox.ebay.com/sell/account/v1'

            # 出荷ポリシーの取得
            fulfillment_response = requests.get(
                f'{base_url}/fulfillment_policy',
                headers=headers,
                params={'marketplace_id': marketplace_id}
            ).json()

            # 支払いポリシーの取得
            payment_response = requests.get(
                f'{base_url}/payment_policy',
                headers=headers,
                params={'marketplace_id': marketplace_id}
            ).json()
            
            # 返品ポリシーの取得
            return_response = requests.get(
                f'{base_url}/return_policy',
                headers=headers,
                params={'marketplace_id': marketplace_id}
            ).json()

            # レスポンスの整形
            policies = {
                'fulfillment_policies': [
                    {
                        'policyId': policy.get('fulfillmentPolicyId'),
                        'name': policy.get('name'),
                        'description': policy.get('description')
                    }
                    for policy in fulfillment_response.get('fulfillmentPolicies', [])
                ],
                'payment_policies': [
                    {
                        'policyId': policy.get('paymentPolicyId'),
                        'name': policy.get('name'),
                        'description': policy.get('description')
                    }
                    for policy in payment_response.get('paymentPolicies', [])
                ],
                'return_policies': [
                    {
                        'policyId': policy.get('returnPolicyId'),
                        'name': policy.get('name'),
                        'description': policy.get('description')
                    }
                    for policy in return_response.get('returnPolicies', [])
                ]
            }

            return Response({
                'success': True,
                'data': policies
            })
            
        except Exception as e:
            logger.error(f"Failed to get policies: {str(e)}")
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

def get_ebay_token():
    try:
        setting = Setting.objects.get()
        
        # トークンの有効期限をチェック
        if setting.ebay_token_expires_at and setting.ebay_token_expires_at > timezone.now():
            return setting.ebay_access_token
            
        # トークンが期限切れの場合はリフレッシュ
        if setting.ebay_refresh_token:
            # リフレッシュトークンを使用して新しいアクセストークンを取得
            new_token = refresh_ebay_token(setting.ebay_refresh_token)
            
            # 新しいトークンを保存
            setting.ebay_access_token = new_token.get('access_token')
            setting.ebay_token_expires_at = timezone.now() + timedelta(seconds=new_token.get('expires_in', 7200))
            setting.save()
            
            return setting.ebay_access_token
            
    except Setting.DoesNotExist:
        raise Exception("eBay設定が見つかりません")
    except Exception as e:
        raise Exception(f"eBayトークンの取得に失敗: {str(e)}")

def refresh_ebay_token(refresh_token, is_sandbox=True):
    setting = Setting.objects.get()
    credentials = f"{setting.ebay_client_id}:{setting.ebay_client_secret}"
    encoded_credentials = b64encode(credentials.encode('utf-8')).decode('utf-8')

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {encoded_credentials}'
    }

    # 環境に応じたスコープとURLを設定
    if is_sandbox:
        BASE_URL = settings.EBAY_SANDBOX_URL
        SCOPES = [
            f'{BASE_URL}/oauth/api_scope',
            f'{BASE_URL}/oauth/api_scope/sell.inventory',
            f'{BASE_URL}/oauth/api_scope/sell.account',
            f'{BASE_URL}/oauth/api_scope/sell.fulfillment'
        ]
        TOKEN_URL = f'{BASE_URL}/identity/v1/oauth2/token'
    else:
        BASE_URL = settings.EBAY_PRODUCTION_URL
        SCOPES = [
            f'{BASE_URL}/oauth/api_scope',
            f'{BASE_URL}/oauth/api_scope/sell.inventory',
            f'{BASE_URL}/oauth/api_scope/sell.account',
            f'{BASE_URL}/oauth/api_scope/sell.fulfillment'
        ]
        TOKEN_URL = f'{BASE_URL}/identity/v1/oauth2/token'

    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'scope': ' '.join(SCOPES)
    }
    TOKEN_URL = 'https://api.sandbox.ebay.com/identity/v1/oauth2/token'
    try:
        response = requests.post(
            TOKEN_URL,
            headers=headers,
            data=data
        )
        
        # デバッグ情報を出力
        print("Request Headers:", {k: v for k, v in headers.items() if k != 'Authorization'})  # 認証情報は隠す
        print("Request Data:", data)
        print("Response Status:", response.status_code)
        print("Response Body:", response.text)

        if response.status_code != 200:
            print(f"eBay API Error: {response.text}")
            
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"eBayトークンのリフレッシュに失敗: {str(e)}")