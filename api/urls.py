from django.urls import path, include
from rest_framework.authtoken import views as token_views
from .views.user import UserListCreateAPIView, UserDetailAPIView
from .views.setting import SettingAPIView
from .views.yahoo_auction import ItemSearchView, ItemDetailView
from .views.shipping_calculator import ShippingCalculatorView
from .views.price_calculator import PriceCalculatorView
from .views.translator import TranslatorView
from .views.test_data import TestDataView
from .views.auth import LoginView, RefreshTokenView, LogoutView
from api.views.ebay_auth import (
    EbayAuthStatusView,
    EbayAuthURLView,
    EbayAuthCallbackView,
    EbayAuthDisconnectView
)

urlpatterns = [
    # 認証関連のエンドポイント
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/refresh/', RefreshTokenView.as_view(), name='auth-refresh'),
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),
    path('users/', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('settings/', SettingAPIView.as_view(), name='settings'),
    path('yahoo-auction/items/', ItemSearchView.as_view(), name='yahoo-auction-item'),
    path('yahoo-auction/detail/', ItemDetailView.as_view(), name='yahoo-auction-detail'),
    path('shipping-calculator/', ShippingCalculatorView.as_view(), name='shipping-calculator'),
    path('price-calculator/', PriceCalculatorView.as_view(), name='price-calculator'),
    path('translate/', TranslatorView.as_view(), name='translate'),
    path('testdata/', TestDataView.as_view(), name='testdata'),
    path('ebay/auth/status/', EbayAuthStatusView.as_view()),
    path('ebay/auth/url/', EbayAuthURLView.as_view()),
    path('ebay/auth/', EbayAuthCallbackView.as_view()),
    path('ebay/auth/disconnect/', EbayAuthDisconnectView.as_view()),
] 