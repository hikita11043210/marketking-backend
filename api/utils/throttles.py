from rest_framework.throttling import UserRateThrottle

class AuctionDetailThrottle(UserRateThrottle):
    scope = 'admin'  # settingsのRATESで'admin'を定義