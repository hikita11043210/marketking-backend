import requests
from bs4 import BeautifulSoup
import logging
import re
from django.conf import settings
import time
from django.utils import timezone
from api.utils.convert_date import convert_yahoo_date
import json
from urllib.parse import urlparse, parse_qs

logger = logging.getLogger(__name__)

class ScrapingService:
    BASE_SEARCH_URL = settings.YAHOO_AUCTION_URL
    MIN_REQUEST_INTERVAL = 3  # 最小リクエスト間隔（秒）
    MAX_RETRIES = 3  # 最大試行回数を追加

    def __init__(self):
        self.session = requests.Session()
        self.last_request_time = None
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'ja,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0'
        })

    def _make_rate_limited_request(self, url, **kwargs):
        """
        レートリミットを考慮したリクエスト実行
        """
        current_time = time.time()
        
        # 前回のリクエストからの経過時間を計算
        if self.last_request_time is not None:
            elapsed = current_time - self.last_request_time
            if elapsed < self.MIN_REQUEST_INTERVAL:
                # 次のリクエストまでの待機時間を計算（小数点以下2桁まで）
                remaining_time = round(self.MIN_REQUEST_INTERVAL - elapsed, 2)
                if remaining_time > 0:
                    logger.info(f"次のリクエストまで {remaining_time} 秒待機")
                    time.sleep(remaining_time)

        # リクエストを実行
        response = self.session.get(url, **kwargs)
        self.last_request_time = time.time()
        return response

    def get_items(self, params):
        """
        Yahoo!オークションの検索を実行し、結果を取得する

        Args:
            params (dict): 検索パラメータ
                min             最低価格
                max             最高価格
                price_type      即決価格 or 入札価格でフィルタ（bidorbuyprice or currentprice）
                p               検索キーワード
                auccat          カテゴリーID
                va              キーワードの強調検索（pと同じ値）
                fixed           表示形式（1:即決価格のみ, 2:オークション形式, 3:両方）
                istatus         商品の状態（3:未使用, 1:中古, 4:目立った傷や汚れなし）
                is_postage_mode 送料無料のみ（0 or 1 デフォルトは0）
                dest_pref_code  配送先の都道府県
                exflg           詳細検索オプションを有効化（0 or 1 デフォルトは1）
                n               1ページの表示件数（50件）
                mode            検索モード（通常検索 = 1）
                brand_id        ブランド指定
                s1              ソート項目（end:終了時間, price:価格, bids:入札数）
                o1              ソート順（a:昇順, d:降順）
                url             検索URL（仮）

        Returns:
            list: 検索結果の商品リスト
        """
        try:
            # デフォルトパラメータの設定
            default_params = {
                'n': '50',  # デフォルトの表示件数
                'mode': '1',  # 通常検索モード
                'exflg': '1',  # 詳細検索オプションを有効化
                'rc_ng': '1',  # 不適切な商品を除外
                'dest_pref_code': '24',  # デフォルトの配送先（三重）
                's1': 'end',  # デフォルトのソート項目（終了時間）
                'o1': 'd',  # デフォルトのソート順（降順）
            }

            # None値を除外しながらパラメータをマージ
            search_params = {k: v for k, v in params.items() if v is not None}

            # 価格パラメータの処理
            if 'min' in search_params and 'max' in search_params:
                min_price = search_params.pop('min')
                max_price = search_params.pop('max')
                fixed_type = search_params.get('fixed', '3')
                price_type = search_params.get('price_type', 'currentprice')

                # 即決価格（bidorbuyprice）の場合
                if price_type == 'bidorbuyprice':
                    if fixed_type == '2' or fixed_type == '3':
                        # オークションとすべての場合は aucmin_bidorbuy_price/aucmax_bidorbuy_price を使用
                        search_params['aucmin_bidorbuy_price'] = min_price
                        search_params['aucmax_bidorbuy_price'] = max_price
                    else:
                        # 定額の場合は aucminprice/aucmaxprice を使用
                        search_params['aucminprice'] = min_price
                        search_params['aucmaxprice'] = max_price
                        if 'price_type' in search_params:
                            del search_params['price_type']

                # 現在価格（currentprice）の場合
                else:
                    if fixed_type == '3':
                        # すべての場合は min/max をそのまま使用
                        search_params['min'] = min_price
                        search_params['max'] = max_price
                    else:
                        # オークションと定額の場合は aucminprice/aucmaxprice を使用
                        search_params['aucminprice'] = min_price
                        search_params['aucmaxprice'] = max_price

            # ブランドIDの処理
            if 'brands' in search_params:
                brand_mapping = {
                    'canon': '100614',
                    'nikon': '101345',
                    'sony': '100614',
                    'fujifilm': '102365',
                    'olympus': '100537',
                    'panasonic': '101460',
                    'pentax': '101475',
                }
                brands = search_params.pop('brands').split(',')
                brand_ids = [brand_mapping[brand.lower()] for brand in brands if brand.lower() in brand_mapping]
                if brand_ids:
                    search_params['brand_id'] = ','.join(sorted(brand_ids))  # IDを昇順でソート
            # brand_idが直接指定された場合はそのまま使用
            elif 'brand_id' in params:
                search_params['brand_id'] = params['brand_id']

            # カテゴリーの処理
            if 'auccat' in search_params and isinstance(search_params['auccat'], str):
                search_params['auccat'] = search_params['auccat'].replace(' ', '')

            # デフォルトパラメータを後から適用（ユーザー指定値を優先）
            for key, value in default_params.items():
                if key not in search_params:
                    search_params[key] = value

            # 商品状態の処理
            if 'item_conditions' in search_params:
                conditions = search_params.pop('item_conditions').split(',')
                if conditions:
                    search_params['istatus'] = ','.join(conditions)

            # 送料無料フラグの処理
            if 'is_free_shipping' in search_params:
                is_free_shipping = search_params.pop('is_free_shipping')
                if is_free_shipping == '1':
                    search_params['is_postage_mode'] = '1'

            # キーワードの強調検索
            if 'p' in search_params:
                search_params['va'] = search_params['p']

            # リクエストURLをログ出力
            # request_url = f"{self.BASE_SEARCH_URL}?{requests.compat.urlencode(search_params)}"
            # print(request_url)

            # 検索結果を取得
            # response = self.session.get(self.BASE_SEARCH_URL, params=search_params)
            # response.raise_for_status()
            # soup = BeautifulSoup(response.text, 'html.parser')

            # URLをパースしてパラメータを取得
            # url = 'https://auctions.yahoo.co.jp/search/search?p=%E3%82%AB%E3%83%A1%E3%83%A9&auccat=23632%2C26318%2C23336&va=%E3%82%AB%E3%83%A1%E3%83%A9&aucmin_bidorbuy_price=10000&aucmax_bidorbuy_price=30000&price_type=bidorbuyprice&min=10000&max=30000&istatus=1%2C4%2C3&is_postage_mode=1&dest_pref_code=24&b=1&n=20&mode=1'
            # url = self.BASE_SEARCH_URL + '?' + requests.compat.urlencode(search_params)
            url = params['url']
            parsed_url = urlparse(url)
            search_params = parse_qs(parsed_url.query)
            
            # 値を文字列化（parse_qsは値をリストで返すため）
            for key, value in search_params.items():
                if isinstance(value, list):
                    search_params[key] = value[0]
            
            response = self._make_rate_limited_request(url, params=search_params)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # #デバッグ用にHTMLを保存（必要に応じてコメントアウト解除）
            # import os, datetime
            # log_dir = "logs/scraping/yahoo_auction/"
            # os.makedirs(log_dir, exist_ok=True)
            # date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            # filename = f"{log_dir}direct_url_{date}.html"
            # with open(filename, "w", encoding="utf-8") as f:
            #     f.write(soup.prettify())

            # 検索結果を解析
            items = self._parse_search_results(soup)

            return {'items': items, 'total_count': len(items)}

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
            response = self.session.get(params.get('url'))
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # import os,datetime
            # log_dir = "logs/scraping/yahoo_auction/"
            # os.makedirs(log_dir, exist_ok=True)
            # date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            # filename = f"{log_dir}detail_{date}.html"
            # with open(filename, "w", encoding="utf-8") as f:
            #     f.write(soup.prettify())

            # 商品基本情報
            data = {}

            # __NEXT_DATA__からJSONデータを取得
            next_data = soup.find('script', {'id': '__NEXT_DATA__'})
            if next_data:
                try:
                    json_data = json.loads(next_data.string)
                    item_detail = json_data.get('props', {}).get('pageProps', {}).get('initialState', {}).get('item', {}).get('detail', {})
                    
                    if item_detail:
                        # 基本情報の取得
                        data['title'] = item_detail.get('title', '')
                        data['auction_id'] = item_detail.get('auctionId', '')
                        data['current_price'] = item_detail.get('price', 0)
                        data['buy_now_price'] = item_detail.get('bidorbuy', 0)
                        data['buy_now_price_in_tax'] = item_detail.get('bidorbuy', 0)
                        data['end_flag'] = item_detail.get('status') == 'closed'
                        
                        # 画像情報の取得
                        images = item_detail.get('img', [])
                        image_urls = [img.get('image') for img in images if img.get('image')]
                        data['images'] = {'url': image_urls}
                        
                        # カテゴリー情報の取得
                        category_path = item_detail.get('category', {}).get('path', [])
                        data['categories'] = [cat.get('name') for cat in category_path if cat.get('name')]
                        
                        # 商品状態
                        data['condition'] = item_detail.get('conditionName', '')
                        
                        # 開始・終了時間
                        data['start_time'] = item_detail.get('startTime', '')
                        data['end_time'] = item_detail.get('endTime', '')
                        
                        # 商品説明
                        data['description'] = item_detail.get('description', [])
                        descriptionHtml = item_detail.get('descriptionHtml', [])
                        descriptionHtml = BeautifulSoup(descriptionHtml, 'html.parser')
                        data['descriptionHtml'] = descriptionHtml.get_text(separator='\n')
                        return data
                except json.JSONDecodeError:
                    logger.warning("JSONデータの解析に失敗しました")

            return data

        except requests.RequestException as e:
            logger.error(f"リクエストエラー: {str(e)}")
            return {'success': False, 'error': e}

        except Exception as e:
            logger.error(f"スクレイピングエラー: {str(e)}")
            return {'success': False, 'error': 'データ解析に失敗しました'}

    def _parse_price_element(self, element):
        """価格要素の解析"""
        # 基本価格抽出
        main_text = element.get_text(strip=True)
        price_match = re.search(r'([\d,]+)円', main_text)
        base_price = int(price_match.group(1).replace(',', '')) if price_match else 0

        # 税情報抽出
        tax_span = element.find('span', class_='Price__tax')
        tax = 0
        tax_included = '税込' in main_text

        if tax_span:
            tax_text = tax_span.get_text(strip=True)
            tax_match = re.search(r'(\d+)', tax_text)
            tax = int(tax_match.group(1)) if tax_match else 0

        return {
            'price_ex_tax': base_price if not tax_included else None,
            'price_in_tax': base_price + tax if not tax_included else base_price,
            'tax_included': tax_included
        }

    def _parse_search_results(self, soup):
        """
        検索結果のHTMLをパースして商品情報を抽出する

        Args:
            soup (BeautifulSoup): パース済みのHTML

        Returns:
            list: 商品情報のリスト
        """
        items = []
        product_list = soup.select('.Product')

        for product in product_list:
            try:
                # 商品情報の抽出
                title_elem = product.select_one('.Product__title')
                url_elem = product.select_one('.Product__titleLink')
                image_elem = product.select_one('.Product__imageData')
                a_elem = product.select_one('.Product__imageLink')

                # 価格情報の取得（現在価格と即決価格を区別）
                price_containers = product.select('.Product__price')
                price_info_containers = product.select('.Product__priceInfo')
                current_price = None
                buy_now_price = None
                
                for container in price_containers:
                    label = container.select_one('.Product__label')
                    price_value = container.select_one('.Product__priceValue')
                    if label and price_value:
                        if '現在' in label.text:
                            current_price = price_value.text.strip().replace('円', '').replace(',', '')
                        elif '即決' in label.text:
                            buy_now_price = price_value.text.strip().replace('円', '').replace(',', '')
                        else:
                            buy_now_price = price_value.text.strip().replace('円', '').replace(',', '')

                for container in price_info_containers:
                    label = container.select_one('.Product__label')
                    price_value = container.select_one('.Product__priceValue')
                    if label and price_value:
                        if '現在' in label.text:
                            current_price = price_value.text.strip().replace('円', '').replace(',', '')
                        elif '即決' in label.text:
                            buy_now_price = price_value.text.strip().replace('円', '').replace(',', '')
                        elif not label.text.strip():  # ラベルが空の場合は固定価格として扱う
                            buy_now_price = price_value.text.strip().replace('円', '').replace(',', '')
                            current_price = buy_now_price  # 固定価格の場合は現在価格も同じ

                seller_elem = product.select_one('.Product__seller')
                end_time_elem = product.select_one('.Product__time')
                bid_count_elem = product.select_one('.Product__bid')
                shipping_elem = product.select_one('.Product__postage')
                condition_elem = product.select_one('.Product__condition')
                location_elem = product.select_one('.Product__location')
                category_elem = product.select_one('.Product__category')
                description_elem = product.select_one('.Product__description')
                payment_elem = product.select_one('.Product__payment')

                if not all([title_elem, url_elem]):
                    continue

                item = {
                    'title': title_elem.text.strip(),
                    'price': current_price,
                    'buy_now_price': buy_now_price,
                    'image_url': image_elem.get('src') if image_elem else None,
                    'url': url_elem.get('href') if url_elem.get('href') else None,
                    'seller': seller_elem.text.strip() if seller_elem else None,
                    'end_time': end_time_elem.text.strip() if end_time_elem else None,
                    'bid_count': bid_count_elem.text.strip() if bid_count_elem else '0',
                    'shipping': shipping_elem.text.strip() if shipping_elem else None,
                    'condition': condition_elem.text.strip() if condition_elem else None,
                    'location': location_elem.text.strip() if location_elem else None,
                    'category': category_elem.text.strip() if category_elem else None,
                    'description': description_elem.text.strip() if description_elem else None,
                    'payment_methods': payment_elem.text.strip() if payment_elem else None,
                    'auction_id': a_elem.get('data-auction-id') if a_elem else None,
                }
                items.append(item)
            except Exception as e:
                logger.warning(f"商品情報の抽出に失敗: {str(e)}")
                continue

        return items 

    def check_item_exist(self, params):
        """
        商品の存在確認と基本情報の取得

        params:
            url: 商品URL

        returns:
            dict: {
                'end_flag': bool,          # 商品が終了しているかどうか
                'current_price': int,      # 現在価格
                'current_price_in_tax': int,  # 現在価格（税込）
                'buy_now_price': int,      # 即決価格
                'buy_now_price_in_tax': int,  # 即決価格（税込）
                'end_time': str,           # 終了時間
                'success': bool            # 処理成功フラグ
            }
        """
        for retry in range(self.MAX_RETRIES):
            try:
                response = self._make_rate_limited_request(
                    params.get('url'),
                    timeout=5,
                    allow_redirects=True
                )

                logger.info(f"リクエスト試行 {retry + 1}/{self.MAX_RETRIES} - URL: {params.get('url')}")
                logger.info(f"ステータスコード: {response.status_code}")

                # 404エラーの場合は商品が存在しない
                if response.status_code == 404:
                    logger.warning(f"商品URLが存在しません: {params.get('url')}")
                    return {
                        'end_flag': True,
                        'success': True
                    }

                if response.status_code == 403:
                    logger.error(f"アクセスが拒否されました (試行 {retry + 1}/{self.MAX_RETRIES})")
                    if retry < self.MAX_RETRIES - 1:
                        continue
                    return {'success': False, 'error': 'アクセスが拒否されました'}

                if response.status_code == 500:
                    logger.error(f"サーバーエラー発生 (試行 {retry + 1}/{self.MAX_RETRIES}) - URL: {params.get('url')}")
                    logger.error(f"レスポンスヘッダー: {dict(response.headers)}")
                    if retry < self.MAX_RETRIES - 1:
                        continue
                    return {'success': False, 'error': 'サーバーエラーが発生しました'}

                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                # import os,datetime
                # log_dir = "logs/scraping/yahoo_auction/"
                # os.makedirs(log_dir, exist_ok=True)
                # date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                # filename = f"{log_dir}check_item_exist_{date}.html"
                # with open(filename, "w", encoding="utf-8") as f:
                #     f.write(soup.prettify())

                result = {
                    'end_flag': False,
                    'current_price': None,
                    'current_price_in_tax': None,
                    'buy_now_price': None,
                    'buy_now_price_in_tax': None,
                    'end_time': None,
                    'success': True
                }

                # __NEXT_DATA__からJSONデータを取得
                next_data = soup.find('script', {'id': '__NEXT_DATA__'})
                if next_data:
                    try:
                        json_data = json.loads(next_data.string)
                        item_detail = json_data.get('props', {}).get('pageProps', {}).get('initialState', {}).get('item', {}).get('detail', {})
                        
                        if item_detail:
                            # 終了判定
                            result['end_flag'] = item_detail.get('status') == 'closed' or item_detail.get('status') == 'cancelled'
                            
                            # 価格情報
                            result['current_price'] = item_detail.get('price', 0)
                            result['current_price_in_tax'] = item_detail.get('price', 0)  # 税込価格が取得できない場合は通常価格を使用
                            result['buy_now_price'] = item_detail.get('bidorbuy', 0)
                            result['buy_now_price_in_tax'] = item_detail.get('bidorbuy', 0)  # 税込価格が取得できない場合は通常価格を使用
                            
                            # 終了時間
                            result['end_time'] = item_detail.get('endTime', '')
                            
                            # # 終了日時が過ぎている場合は終了フラグを立てる
                            # if result['end_time']:
                            #     end_time = convert_yahoo_date(result['end_time'])
                            #     if end_time < timezone.now():
                            #         result['end_flag'] = True
                            return result

                    except json.JSONDecodeError:
                        logger.warning("JSONデータの解析に失敗しました")
                        return {'success': False, 'error': 'JSONデータの解析に失敗しました'}

                return result

            except requests.Timeout:
                logger.warning(f"タイムアウト発生 (試行 {retry + 1}/{self.MAX_RETRIES}) - URL: {params.get('url')}")
                if retry < self.MAX_RETRIES - 1:
                    continue
                return {'success': False, 'error': 'タイムアウトが発生しました'}

            except requests.RequestException as e:
                logger.error(f"リクエストエラー (試行 {retry + 1}/{self.MAX_RETRIES}) - URL: {params.get('url')}")
                logger.error(f"エラーの種類: {type(e).__name__}")
                logger.error(f"エラーの詳細: {str(e)}")
                if retry < self.MAX_RETRIES - 1:
                    continue
                return {'success': False, 'error': str(e)}

            except Exception as e:
                logger.error(f"スクレイピングエラー (試行 {retry + 1}/{self.MAX_RETRIES}) - URL: {params.get('url')}")
                logger.error(f"エラーの種類: {type(e).__name__}")
                logger.error(f"エラーの詳細: {str(e)}")
                if retry < self.MAX_RETRIES - 1:
                    continue
                return {'success': False, 'error': str(e)} 