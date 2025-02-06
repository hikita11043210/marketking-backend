from ebaysdk.trading import Connection as Trading
from django.conf import settings
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
from django.conf import settings
import json
from ..models import Setting
from django.utils import timezone
import requests
from base64 import b64encode
import time

class TestDataView(APIView):
    def post(self, request):
        try:
            token = request.data.get('token')
            if not token:
                return Response({
                    'success': False,
                    'message': 'トークンが必要です'
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Account APIのエンドポイント
                base_url = 'https://api.sandbox.ebay.com'
                
                # 既存のポリシーを確認
                headers = {
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }

                # マーケットプレイスIDを指定してポリシーを取得 
                payment_policies = requests.get(
                    f'{base_url}/sell/account/v1/payment_policy?marketplace_id=EBAY_JP',
                    headers=headers
                )
                print("Current Payment Policies:", payment_policies.text)

                if payment_policies.status_code != 200:
                    return Response({
                        'success': False,
                        'message': 'ビジネスポリシーが有効化されていません。eBayのウェブサイトで有効化してください。',
                        'error': payment_policies.json()
                    }, status=status.HTTP_400_BAD_REQUEST)

                # 支払いポリシーの作成
                payment_policy = {
                    "name": "テスト支払いポリシー",
                    "description": "テスト用の支払いポリシーです",
                    "marketplaceId": "EBAY_JP",
                    "categoryTypes": [
                        {
                            "name": "ALL_EXCLUDING_MOTORS_VEHICLES"
                        }
                    ],
                    "immediatePay": True
                }

                # 支払いポリシーの登録
                policy_response = requests.post(
                    f'{base_url}/sell/account/v1/payment_policy',
                    headers=headers,
                    data=json.dumps(payment_policy)
                )

                print("Policy Response:", policy_response.text)  # デバッグ用

                if policy_response.status_code == 201:
                    return Response({
                        'success': True,
                        'message': 'テスト支払いポリシーの登録が完了しました',
                        'data': policy_response.json()
                    })
                else:
                    return Response({
                        'success': False,
                        'message': '支払いポリシー登録に失敗しました',
                        'error': policy_response.json()
                    }, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                return Response({
                    'success': False,
                    'message': 'API処理エラー',
                    'error': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'success': False,
                'message': 'ポリシー登録に失敗しました',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)