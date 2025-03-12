import requests
from bs4 import BeautifulSoup
import logging
import re
from django.conf import settings
from api.utils.generate_log_file import generate_log_file
import json
logger = logging.getLogger(__name__)

class ScrapingService:
    BASE_SEARCH_URL = settings.YAHOO_FREE_MARKET_URL
    BASE_ITEM_URL = settings.YAHOO_FREE_MARKET_URL

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def get_items(self, params):
        """
        Yahoo!フリーマーケットの検索を実行し、結果を取得する

        Args:
            params (dict): 検索パラメータ
                - searchText: 検索テキスト
                - page: ページ数（デフォルト1）
                - open: 販売中の商品
                - minPrice: 最低価格
                - maxPrice: 最高価格
                - condition: 状態
        Returns:
            dict: 検索結果と総件数を含む辞書
        """
        try:
            # 検索テキストの取得
            search_text = params.get('searchText', '')
            if not search_text:
                raise ValueError("検索テキストは必須です")

            # 検索URLの構築
            search_url = f"{self.BASE_SEARCH_URL}{search_text}"
            
            # クエリパラメータの設定
            query_params = {
                'open': '1',  # 販売中の商品のみに固定
                'page': params.get('page', '1'),  # ページ番号
                # 'sold': '1'   # 売切れの商品
            }

            # 商品状態の設定
            conditions = params.get('conditions', [])
            if conditions:
                if isinstance(conditions, str):
                    conditions = [conditions]
                if len(conditions) > 0:
                    query_params['conditions'] = '%2C'.join(conditions)

            # 価格範囲の設定
            min_price = params.get('minPrice')
            max_price = params.get('maxPrice')
            if min_price is not None:
                query_params['minPrice'] = str(min_price)
            if max_price is not None:
                query_params['maxPrice'] = str(max_price)

            # 最初のページを取得して総件数を確認
            first_page = self.session.get(search_url, params=query_params)
            first_page.raise_for_status()
            soup = BeautifulSoup(first_page.text, 'html.parser')

            # import os,datetime
            # log_dir = "logs/scraping/yahoo_free_market/"
            # os.makedirs(log_dir, exist_ok=True)
            # filename = f"{log_dir}list_{datetime.datetime.now()}.html"
            # with open(filename, "w", encoding="utf-8") as f:
            #     f.write(soup.prettify())
            #     logger.info(f"Soup内容を {filename} に保存しました")

            # 最初のページの結果を解析
            items = self._parse_search_results(soup)

            return {
                'items': items,
                'total': len(items)
            }

        except requests.RequestException as e:
            logger.error(f"リクエストエラー: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"スクレイピングエラー: {str(e)}")
            raise

    def get_item_detail(self, params):
        """
        商品詳細情報をスクレイピング
        """
        try:
            item_id = params.get('item_id')
            response = self.session.get(f'https://paypayfleamarket.yahoo.co.jp/item/{item_id}')
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # import os,datetime
            # log_dir = "logs/scraping/yahoo_free_market/"
            # os.makedirs(log_dir, exist_ok=True)
            # filename = f"{log_dir}detail_{datetime.datetime.now()}.html"
            # with open(filename, "w", encoding="utf-8") as f:
            #     f.write(soup.prettify())
            #     logger.info(f"Soup内容を {filename} に保存しました")

            # __NEXT_DATA__スクリプトを取得
            next_data_script = soup.find('script', {'id': '__NEXT_DATA__'})
            if not next_data_script:
                raise ValueError("商品データが見つかりません")

            json_data = json.loads(next_data_script.string)
            
            # 商品情報を取得
            item_data = json_data.get('props', {}).get('initialState', {}).get('itemsState', {}).get('items', {}).get('item', {})
            if not item_data:
                raise ValueError("商品情報が見つかりません")

            # 必要な情報を抽出
            data = {
                'title': item_data.get('title', ''),
                'description': item_data.get('description', ''),
                'images': [img.get('url', '') for img in item_data.get('images', [])],
                'price': item_data.get('price', 0),
                'item_id': item_data.get('id', ''),
                'url': self.BASE_ITEM_URL + item_id,
                'condition': item_data.get('condition', {}).get('text', ''),
                'category': [category.get('name', '') for category in item_data.get('categoryList', [])],
                'delivery_schedule': item_data.get('deliverySchedule', {}).get('text', ''),
                'delivery_method': item_data.get('deliveryMethod', {}).get('text', ''),
                'create_date': item_data.get('createDate', ''),
                'update_date': item_data.get('updateDate', ''),
                'status': item_data.get('status', ''),
                'pv_count': item_data.get('pvCount', 0),
                'like_count': item_data.get('likeCount', 0),
            }

            # 必須キーの定義
            required_keys = [
                'title',
                'description',
                'images',
                'price',
                'item_id',
                'condition',
                'delivery_schedule',
                'delivery_method'
            ]

            # 存在しないキーを確認
            missing_keys = []
            for key in required_keys:
                if key not in data or data[key] == '' or data[key] == [] or data[key] == {}:
                    missing_keys.append(key)

            return data

        except requests.RequestException as e:
            logger.error(f"リクエストエラー: {str(e)}")
            return {'success': False, 'error': str(e)}

        except Exception as e:
            logger.error(f"スクレイピングエラー: {str(e)}")
            return {'success': False, 'error': 'データ解析に失敗しました'}


    def _parse_search_results(self, soup):
        """
        検索結果のHTMLをパースして商品情報を抽出する

        Args:
            soup (BeautifulSoup): パース済みのHTML

        Returns:
            list: 商品情報のリスト（サムネイル、アイテムID、価格）
        """
        items = []
        # 商品一覧のコンテナを取得
        product_container = soup.find('div', id='itm')
        if not product_container:
            logger.error("商品一覧のコンテナが見つかりません")
            return items
        # 各商品のリンク要素を取得
        product_links = product_container.find_all('a', href=lambda x: x and '/item/' in x)
        for link in product_links:
            try:
                # アイテムID（URLから抽出）
                item_id = None
                if 'href' in link.attrs:
                    url_match = re.search(r'/item/([a-zA-Z0-9]+)', link['href'])
                    if url_match:
                        item_id = url_match.group(1)

                # サムネイル画像
                thumbnail_elem = link.find('img')
                thumbnail_url = None
                if thumbnail_elem and thumbnail_elem.get('src'):
                    # .jpg以降のクエリパラメータを削除
                    src = thumbnail_elem.get('src')
                    jpg_index = src.find('.jpg')
                    if jpg_index != -1:
                        thumbnail_url = src[:jpg_index + 4]  # .jpgまでを含める

                # 商品価格
                price_elem = link.find('p')
                price = None
                if price_elem:
                    price_text = price_elem.text.strip()
                    price_match = re.search(r'([0-9,]+)', price_text)
                    if price_match:
                        price = int(price_match.group(1).replace(',', ''))

                if all([thumbnail_url, item_id, price]):
                    items.append({
                        'thumbnail_url': thumbnail_url,
                        'item_id': item_id,
                        'price': price
                    })

            except Exception as e:
                logger.error(f"商品情報の抽出に失敗: {str(e)}")
                continue

        return items 
    

    def check_item_exist(self, params):
        """
        商品が存在するかどうかを確認する

        params:
            item_id: 商品ID

        returns:
            bool: 商品が存在するかどうか
        """
        try:
            item_id = params.get('item_id')
            response = self.session.get(f'https://paypayfleamarket.yahoo.co.jp/item/{item_id}')

            # 結果が存在しない場合（出品取消しをされた場合かもしれない）
            if response.status_code == 404:
                logger.warning(f"商品ID {item_id} は存在しません")
                return True

            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # import os,datetime
            # log_dir = "logs/scraping/yahoo_free_market/"
            # os.makedirs(log_dir, exist_ok=True)
            # filename = f"{log_dir}check_{item_id}_{datetime.datetime.now()}.html"
            # with open(filename, "w", encoding="utf-8") as f:
            #     f.write(soup.prettify())
            #     logger.info(f"Soup内容を {filename} に保存しました")

            # __NEXT_DATA__スクリプトを取得
            next_data_script = soup.find('script', {'id': '__NEXT_DATA__'})
            if not next_data_script:
                return True

            # 売り切れフラグの判定
            if bool(soup.find('img', class_='sc-7fc76147-7 bpVTgE')):
                return True

            return False

        except requests.RequestException as e:
            logger.error(f"check_item_exist_リクエストエラー: {str(e)}")
            return {'success': False, 'error': str(e)}

        except Exception as e:
            logger.error(f"check_item_exist_スクレイピングエラー: {str(e)}")
            return {'success': False, 'error': 'データ解析に失敗しました'}