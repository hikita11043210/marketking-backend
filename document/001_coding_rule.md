### ✅ DRF開発ルール：フォルダ構造と責務（views + use_cases + services）

---

#### 📁 `views/` - APIエンドポイントの受け口

- HTTPリクエストの受け取りとレスポンスの返却のみを担当
- 直接ビジネスロジックを実装しない
- `use_cases`に処理を委譲する
- 例外処理を行い、適切なHTTPステータスで返却する
- 必要に応じてログ出力（`logger.exception`）

```python
class PurchaseAPIView(APIView):
    def post(self, request):
        try:
            result = handle_purchase(request.data)
            return Response(result, status=200)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)
        except Exception as e:
            logger.exception("Unexpected error")
            return Response({"error": "Internal server error"}, status=500)
```

---

#### 📁 `use_cases/` - 業務処理の流れを定義（調整役）

- 複数のserviceを組み合わせ、業務的な操作（ユースケース）を実現する
- 処理の順序・条件分岐・例外の補足などを担う
- 原則として、**各use_caseは1つの目的（仕入れる、キャンセルする 等）を持つ**

```python
def handle_purchase(data):
    product_info = scrape_product_data(data["url"])
    product = register_product(product_info)
    update_purchase_status(product.id)
    return {"product_id": product.id}
```

---

#### 📁 `services/` - 単一責務のドメイン処理を担当

- 実際のロジックを実行する（スクレイピング・DB登録・状態更新など）
- 各関数（またはクラス）は**「1つの明確な目的」**を持つこと
- 再利用性の高い処理を書くこと（例：外部API呼び出しなど）
- 必要に応じて想定されるエラーを補足し、ValueError等に変換して上層へ渡す

```python
def register_product(info):
    try:
        return Product.objects.create(**info)
    except IntegrityError:
        raise ValueError("Product registration failed")
```

---

#### 📁 `common/` - 共通機能・ヘルパーの配置

- フロントエンドとの連携に必要な共通処理を実装
- 再利用性の高いユーティリティ関数
- ミックスインやヘルパークラス
- フォルダ構成:
  - `common/mixins/`: ビュー拡張用のミックスインクラス
  - `common/response_helpers.py`: レスポンス生成ヘルパー関数
  - `common/exceptions.py`: 例外ハンドラ

```python
# common/mixins/response.py
class ResponseMixin:
    """DRFビューの拡張用ミックスイン"""
    
    def success_response(self, data=None, message="処理が完了しました", status_code=status.HTTP_200_OK):
        """成功レスポンスを返す"""
        return success_response(data, message, status_code)
```

---

### 🌟 共通レスポンス処理の利用ルール

1. **全てのビューでミックスインを使用すること**:
   ```python
   from api.common.mixins.response import ResponseMixin
   
   class MyAPIView(APIView, ResponseMixin):
       # ...
   ```

2. **レスポンス形式の統一**:
   - 成功レスポンス: `self.success_response(data, message)`
   - エラーレスポンス: `self.error_response(exception, message, status_code)`
   - バリデーションエラー: `self.validation_error_response(errors, message)`

3. **ページネーション**:
   - リスト表示の場合は`PaginationMixin`を使用すること
   ```python
   from api.common.mixins.response import ResponseMixin, PaginationMixin
   
   class ProductListView(ListAPIView, ResponseMixin, PaginationMixin):
       # ...
   ```

4. **例外ハンドラによる自動変換**:
   - DRF標準例外は自動的に共通フォーマットに変換されます
   - カスタム例外を作成する場合は、適切な例外クラスを継承すること


### 📦 フォルダ構成例

```
api/
├── views/ # APIエンドポイント
├── use_cases/ # ビジネスロジックの流れ定義
├── services/ # 個別ドメイン処理
├── models/ # DBモデル定義
├── common/ # 共通処理
│ ├── mixins/ # ミックスインクラス
│ │ └── response.py # レスポンス処理ミックスイン
│ ├── response_helpers.py # レスポンス生成関数
│ └── exceptions.py # 例外ハンドラ
├── serializers/ # データシリアライザ
└── urls.py # URL定義
```

---

### ✅ 命名ルール（簡易）

- use case：`handle_〇〇`, `process_〇〇`
- service関数：`〇〇_service.py`内に、`create_x`, `update_x`, `scrape_x`など
- API view：`〇〇APIView`のクラス名を使用

---
