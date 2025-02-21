from rest_framework.views import APIView
from api.services.ebay.trading import Trading
from api.utils.response_helpers import create_success_response, create_error_response
from api.services.ebay.category import Category
from rest_framework import status

class EbayCategoryItemSpecificsView(APIView):
    def get(self, request):
        try:
            category_id = request.query_params.get('categoryId')
            trading_api = Trading(request.user)
            ebay_service_category = Category(request.user)
            category_tree_id = ebay_service_category.get_categories_tree_id()
            result = trading_api.get_category_aspects(
                category_id=category_id,
                category_tree_id=category_tree_id
            )

            return create_success_response(data=result, message="カテゴリ固有の仕様情報を取得しました")

        except Exception as e:
            return create_error_response(str(e))
