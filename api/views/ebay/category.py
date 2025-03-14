from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.services.ebay.category import Category
from api.utils.throttles import AuctionDetailThrottle
from api.utils.response_helpers import create_success_response, create_error_response

class EbayCategoryView(APIView):
    """eBayのカテゴリ情報を取得するView"""
    permission_classes = [IsAuthenticated]
    throttle_classes = [AuctionDetailThrottle]

    def get(self, request):
        # 検索クエリがある場合は検索を実行
        query = request.query_params.get('q')
        ebay_service_category = Category(request.user)
        category_tree_id = ebay_service_category.get_categories_tree_id()
        try:
            if query:
                # カテゴリ検索
                result = ebay_service_category.get_categories(category_tree_id, query)
            else:
                # 全カテゴリ取得
                result = ebay_service_category.get_all_categories(category_tree_id)
            return create_success_response(
                data=result,
                message='カテゴリ情報を取得しました'
            )
        except Exception as e:
            return create_error_response(e)
