from django.urls import path
from .views.master.setting import SettingAPIView
from .views.yahoo_auction.search import SearchView as YahooAuctionSearchView
from .views.yahoo_auction.register import ItemDetailView, RegisterView
from .views.utils.calculator_shipping import CalculatorShippingView
from .views.utils.calculator_price import CalculatorPriceView
from .views.utils.translator import TranslatorView
from .views.login import LoginView, RefreshTokenView, LogoutView
from .views.ebay.auth import (
    EbayAuthStatusView,
    EbayAuthURLView,
    EbayAuthCallbackView,
    EbayAuthDisconnectView
)
from .views.ebay.policies import EbayPoliciesView
from .views.ebay.category import EbayCategoryView
from .views.ebay.itemSpecifics import EbayItemSpecificsView
from .views.ebay.condition import EbayConditionView
from .views.yahoo_auction.list import ListView, SynchronizeYahooAuctionView
from .views.ebay.offer import OfferView
from .views.ebay.categoryItemSpecifics import EbayCategoryItemSpecificsView
from .views.synchronize.script import SynchronizeScriptView
from .views.yahoo_free_market.search import YahooFreeMarketSearchView
from .views.yahoo_free_market.register import YahooFreeMarketItemDetailView, YahooFreeMarketRegisterView
from .views.yahoo_free_market.list import YahooFreeMarketListView, SynchronizeYahooFreeMarketView
from .views.ebay.list import SynchronizeEbayView
# 古物台帳関連のビューをインポート
from .views.antique_ledger.transaction_type import TransactionTypeListAPIView
from .views.antique_ledger.transaction import TransactionListCreateAPIView, TransactionDetailAPIView
from .views.yahoo_auction import YahooAuctionStatusUpdateAPIView
from .views.yahoo_free_market import YahooFreeMarketStatusUpdateAPIView

urlpatterns = [
    # 認証関連のエンドポイント
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/refresh/', RefreshTokenView.as_view(), name='auth-refresh'),
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),
    path('settings/', SettingAPIView.as_view(), name='settings'),
    path('yahoo-auction/items/', YahooAuctionSearchView.as_view(), name='yahoo-auction-item'),
    path('yahoo-auction/detail/', ItemDetailView.as_view(), name='yahoo-auction-detail'),
    path('shipping-calculator/', CalculatorShippingView.as_view(), name='shipping-calculator'),
    path('calculator-price/', CalculatorPriceView.as_view(), name='calculator-price'),
    path('translate/', TranslatorView.as_view(), name='translate'),
    path('ebay/auth/status/', EbayAuthStatusView.as_view()),
    path('ebay/auth/url/', EbayAuthURLView.as_view()),
    path('ebay/auth/', EbayAuthCallbackView.as_view()),
    path('ebay/auth/disconnect/', EbayAuthDisconnectView.as_view()),
    path('ebay/categoryItemSpecifics/', EbayCategoryItemSpecificsView.as_view()),
    path('ebay/policies/', EbayPoliciesView.as_view()),
    path('ebay/category/', EbayCategoryView.as_view()),
    path('ebay/itemSpecifics/', EbayItemSpecificsView.as_view()),
    path('ebay/register/', RegisterView.as_view()),
    path('ebay/condition/', EbayConditionView.as_view()),
    path('list/', ListView.as_view()),
    path('ebay/offer/', OfferView.as_view()),
    path('synchronize/ebay/', SynchronizeEbayView.as_view()),
    path('synchronize/yahoo-auction/', SynchronizeYahooAuctionView.as_view()),
    path('synchronize/yahoo-free-market/', SynchronizeYahooFreeMarketView.as_view()),
    path('synchronize/script/', SynchronizeScriptView.as_view()),
    path('yahoo-free-market/search/', YahooFreeMarketSearchView.as_view(), name='yahoo-free-market-search'),
    path('yahoo-free-market/detail/', YahooFreeMarketItemDetailView.as_view(), name='yahoo-free-market-detail'),
    path('yahoo-free-market/register/', YahooFreeMarketRegisterView.as_view(), name='yahoo-free-market-register'),
    path('yahoo-free-market/list/', YahooFreeMarketListView.as_view(), name='yahoo-free-market-list'),
    path('yahoo-free-market/delete/', YahooFreeMarketListView.as_view(), name='yahoo-free-market-delete'),
    
    # ステータス更新エンドポイント
    path('yahoo-auction/status-update/<int:pk>/', YahooAuctionStatusUpdateAPIView.as_view(), name='yahoo-auction-status-update'),
    path('yahoo-free-market/status-update/<int:pk>/', YahooFreeMarketStatusUpdateAPIView.as_view(), name='yahoo-free-market-status-update'),
    
    # 古物台帳関連のエンドポイント
    path('antique-ledger/transaction-types/', TransactionTypeListAPIView.as_view(), name='transaction-types'),
    path('antique-ledger/transactions/', TransactionListCreateAPIView.as_view(), name='transaction-list-create'),
    path('antique-ledger/transactions/<int:pk>/', TransactionDetailAPIView.as_view(), name='transaction-detail'),
] 