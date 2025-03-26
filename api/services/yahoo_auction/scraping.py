import requests
from bs4 import BeautifulSoup
import logging
import re
from django.conf import settings
logger = logging.getLogger(__name__)

class ScrapingService:
    BASE_SEARCH_URL = settings.YAHOO_AUCTION_URL

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

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
            response = self.session.get(self.BASE_SEARCH_URL, params=search_params)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # import os,datetime
            # log_dir = "logs/scraping/yahoo_auction/"
            # os.makedirs(log_dir, exist_ok=True)
            # date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            # filename = f"{log_dir}list_{date}.html"
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

            # 終了判定
            closed_header = soup.find('div', class_='ClosedHeader')
            if closed_header is not None:  # Noneチェックを追加
                if 'このオークションは終了しています' in closed_header.get_text():
                    data['end_flag'] = True
            else:
                data['end_flag'] = False
            
            # タイトル
            data['title'] = ''
            title_elem = soup.find('h1', class_='ProductTitle__text')
            if title_elem:
                data['title'] = title_elem.get_text(strip=True)

            # 商品説明の取得
            description_elem = soup.find('div', class_='ProductExplanation__commentBody')
            if description_elem:
                # 改行を保持するためstrip=Trueを削除し、<br>タグを改行に変換
                for br in description_elem.find_all('br'):
                    br.replace_with('\n')
                # 連続する改行を単一の改行に変換
                raw_text = description_elem.get_text(strip=False)
                cleaned_text = re.sub(r'\n+', '\n', raw_text)
                data['description'] = cleaned_text.strip()
            else:
                data['description'] = ''

            # 商品価格
            data['current_price'] = ''
            data['current_price_in_tax'] = ''
            data['buy_now_price'] = ''
            data['buy_now_price_in_tax'] = ''
            price_rows = soup.find_all('div', class_='Price__row')
            for row in price_rows:
                title = row.find('dt', class_='Price__title')
                if not title:
                    continue
                value = row.find('dd', class_='Price__value')
                if not value:
                    continue
                    
                # 価格タイトル（現在/即決/定額など）
                title_text = title.text.strip() if title else ''
                
                # 価格テキストの処理（カンマ、円記号、空白を削除）
                price_text = value.get_text(strip=True)
                price = ''
                price_in_tax = '0'
                
                # 基本価格の抽出
                if '円' in price_text:
                    price = price_text.split('円')[0].replace(',', '').strip()
                
                # 税込み価格の抽出（複数のパターンに対応）
                tax_span = value.find('span', class_='Price__tax')
                if tax_span:
                    tax_text = tax_span.get_text(strip=True)
                    
                    # パターン1: （税込 X 円）
                    if '税込' in tax_text and '円' in tax_text:
                        try:
                            # 「税込」と「円」の間の数値を抽出
                            tax_parts = tax_text.split('税込')[1].split('円')[0]
                            price_in_tax = tax_parts.replace(',', '').strip()
                        except (IndexError, ValueError):
                            price_in_tax = '0'
                    
                    # パターン2: （税 X 円）
                    elif '税' in tax_text and '円' in tax_text:
                        try:
                            # 「税」と「円」の間の数値を抽出
                            tax_parts = tax_text.split('税')[1].split('円')[0]
                            # 税額だけの場合は、本体価格に加算して税込み価格を計算
                            tax_amount = tax_parts.replace(',', '').strip()
                            try:
                                price_in_tax = str(int(price) + int(tax_amount))
                            except (ValueError, TypeError):
                                price_in_tax = price  # 変換エラー時は本体価格をそのまま使用
                        except (IndexError, ValueError):
                            price_in_tax = price  # エラー時は本体価格をそのまま使用
                
                # 価格情報がない場合はスキップ
                if not price:
                    continue
                    
                # 現在価格（オークション形式の場合）
                if '現在' in title_text:
                    data['current_price'] = int(price)
                    data['current_price_in_tax'] = int(price_in_tax)
                # 即決価格または定額価格（固定価格形式の場合）
                elif '即決' in title_text or '価格' in title_text or title_text == '':
                    data['buy_now_price'] = int(price)
                    data['buy_now_price_in_tax'] = int(price_in_tax)

            # 商品詳細テーブルの解析
            price_rows = soup.find_all('tr', class_='Section__tableRow')
            for row in price_rows:
                tableHead = row.find('th', class_='Section__tableHead')
                tableData = row.find('td', class_='Section__tableData')
                if not tableHead or not tableData:
                    continue

                title_text = tableHead.get_text(strip=True)

                if title_text == 'オークションID':
                    data['auction_id'] = tableData.get_text(strip=True)
                elif title_text == 'カテゴリ':
                    categories = tableData.find_all('a')
                    data['categories'] = [cat.get_text(strip=True) for cat in categories]
                elif title_text == '状態':
                    condition = tableData.find('a')
                    data['condition'] = condition.get_text(strip=True)
                elif title_text == '開始日時':
                    data['start_time'] = tableData.get_text(strip=True)
                elif title_text == '終了日時':
                    data['end_time'] = tableData.get_text(strip=True)

            # 画像取得部分の修正
            image_elements = soup.select('li.ProductImage__image img, div.Thumbnail__item img')
            all_images = set()
            for img in image_elements:
                # 通常のsrc属性と遅延読み込み用のdata-srcをチェック
                image_url = img.get('data-src') or img.get('src')
                if image_url and 'auctions.c.yimg.jp' in image_url:
                    all_images.add(image_url)

            # 画像URLを整理
            sorted_images = sorted(
                all_images, 
                key=lambda x: int(re.search(r'(\d+)\.jpg', x).group(1)) if re.search(r'(\d+)\.jpg', x) else 0
            )
            data['images'] = {
                'url': sorted_images
            }

            # 必須キーの定義
            required_keys = [
                'title',
                'current_price',
                'current_price_in_tax',
                'buy_now_price',
                'buy_now_price_in_tax',
                'start_time',
                'end_time',
                'auction_id',
                'categories',
                'condition',
                'images',
                'description'
            ]

            # 存在しないキーを確認
            missing_keys = []
            for key in required_keys:
                if key not in data or data[key] == '':
                    missing_keys.append(key)

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