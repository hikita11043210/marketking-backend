from django.urls import path, include
from rest_framework.authtoken import views as token_views
from .views.user import UserListCreateAPIView, UserDetailAPIView
from .views.setting import SettingAPIView
from .views.scraping import YahooAuctionItemSearchView, YahooAuctionCategorySearchView, YahooAuctionDetailView
from .views.shipping_calculator import ShippingCalculatorView
from .views.price_calculator import PriceCalculatorView
from .views.ebay import (
    EbayAuthView,
    EbayRegisterView,
    EbayCategoriesView,
    EbayPoliciesView
)
from .views.test_data import TestDataView

urlpatterns = [
    path('token/', token_views.obtain_auth_token),  # ログイン用エンドポイント
    path('users/', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('settings/', SettingAPIView.as_view(), name='settings'),
    path('search/yahoo-auction/items/', YahooAuctionItemSearchView.as_view(), name='yahoo-auction-item-search'),
    path('search/yahoo-auction/detail/', YahooAuctionDetailView.as_view(), name='yahoo-auction-detail'),
    path('search/yahoo-auction/categories/', YahooAuctionCategorySearchView.as_view(), name='yahoo-auction-category-search'),
    path('shipping-calculator/', ShippingCalculatorView.as_view(), name='shipping-calculator'),
    path('price-calculator/', PriceCalculatorView.as_view(), name='price-calculator'),
    path('ebay/auth/', EbayAuthView.as_view(), name='ebay-auth'),
    path('ebay/register/', EbayRegisterView.as_view(), name='ebay-register'),
    path('ebay/categories/', EbayCategoriesView.as_view(), name='ebay-categories'),
    path('ebay/policies/', EbayPoliciesView.as_view(), name='ebay-policies'),
    path('testdata/', TestDataView.as_view(), name='testdata'),
] 