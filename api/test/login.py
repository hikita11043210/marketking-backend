from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.db import connection
User = get_user_model()

class LoginTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """テストユーザー作成"""
        User.objects.all().delete()
        # ユーザー作成処理
        try:
            cls.user = User.objects.create_user(
                username='testuser',
                password='testpassword123',
                email='test@example.com'
            )
        except Exception as e:
            raise
        
        # URL解決
        # cls.login_url = reverse('auth-login')

    # def test_successful_login_flow(self):
    #     """エンドポイント経由の正常系テスト"""
    #     response = self.client.post(
    #         self.login_url,
    #         {'username': 'toshiki', 'password': 'password'},
    #         format='json'
    #     )
        
    #     # ステータスコード検証
    #     self.assertEqual(response.status_code, 200)
        
    #     # レスポンスデータ構造検証
    #     self.assertIn('accessToken', response.data)
    #     self.assertIn('refreshToken', response.data)
        
    #     # ユーザー情報検証
    #     user_data = response.data['user']
    #     self.assertEqual(user_data['username'], 'toshiki')
    #     self.assertEqual(user_data['email'], 'toshiki@example.com')
        
    #     # Cookie設定検証
    #     cookies = response.client.cookies
    #     self.assertIsNotNone(cookies.get('jwt'))
    #     self.assertIsNotNone(cookies.get('jwt_refresh'))
    #     self.assertTrue(cookies['jwt']['httponly'])
    #     self.assertEqual(cookies['jwt']['samesite'], 'Lax')