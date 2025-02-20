from django.urls import path
from .views.setting import SettingAPIView
from .views.yahoo_auction import ItemSearchView, ItemDetailView
from .views.shipping_calculator import ShippingCalculatorView
from .views.calculator_price import CalculatorPriceView
from .views.translator import TranslatorView
from .views.auth import LoginView, RefreshTokenView, LogoutView
from .views.ebay.auth import (
    EbayAuthStatusView,
    EbayAuthURLView,
    EbayAuthCallbackView,
    EbayAuthDisconnectView
)
from .views.ebay.policies import EbayPoliciesView
from .views.ebay.category import EbayCategoryView
from .views.ebay.itemSpecifics import EbayItemSpecificsView
from .views.ebay.register import EbayRegisterView
from .views.ebay.condition import EbayConditionView
from .views.ebay.list import List
from .views.ebay.offer import OfferView

urlpatterns = [
    # 認証関連のエンドポイント
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/refresh/', RefreshTokenView.as_view(), name='auth-refresh'),
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),
    path('settings/', SettingAPIView.as_view(), name='settings'),
    path('yahoo-auction/items/', ItemSearchView.as_view(), name='yahoo-auction-item'),
    path('yahoo-auction/detail/', ItemDetailView.as_view(), name='yahoo-auction-detail'),
    path('shipping-calculator/', ShippingCalculatorView.as_view(), name='shipping-calculator'),
    path('calculator-price/', CalculatorPriceView.as_view(), name='calculator-price'),
    path('translate/', TranslatorView.as_view(), name='translate'),
    path('ebay/auth/status/', EbayAuthStatusView.as_view()),
    path('ebay/auth/url/', EbayAuthURLView.as_view()),
    path('ebay/auth/', EbayAuthCallbackView.as_view()),
    path('ebay/auth/disconnect/', EbayAuthDisconnectView.as_view()),
    path('ebay/policies/', EbayPoliciesView.as_view()),
    path('ebay/category/', EbayCategoryView.as_view()),
    path('ebay/itemSpecifics/', EbayItemSpecificsView.as_view()),
    path('ebay/register/', EbayRegisterView.as_view()),
    path('ebay/condition/', EbayConditionView.as_view()),
    path('list/', List.as_view()),
    path('ebay/offer/', OfferView.as_view()),

] 