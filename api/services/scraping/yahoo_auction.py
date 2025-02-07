import requests
from bs4 import BeautifulSoup
import logging
import json
from json.decoder import JSONDecodeError
from datetime import datetime
import re
logger = logging.getLogger(__name__)

class YahooAuctionService:
    BASE_URL = "https://auctions.yahoo.co.jp/search/search"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def search_items(self, params):
        """
        Yahoo!オークションの検索を実行し、結果を取得する

        Args:
            params (dict): 検索パラメータ
                - p: 検索キーワード
                - auccat: カテゴリ指定
                - va: キーワードフィルター
                - price_type: 現在価格/即決価格
                - min: 価格下限
                - max: 価格上限
                - istatus: オークション状態
                - new: 新着商品フィルター
                - is_postage_mode: 送料設定フィルター
                - dest_pref_code: 配送先都道府県コード
                - fixed: 出品形式
                - exflg: エクスプレスオークション
                - b: 開始番号
                - n: 取得件数

        Returns:
            dict: 検索結果と総件数を含む辞書
        """
        try:
            # デフォルトパラメータの設定
            default_params = {
            }

            # None値を除外しながらパラメータをマージ
            search_params = {k: v for k, v in params.items() if v is not None}
            search_params.update(default_params)

            # 最初のページを取得して総件数を確認
            first_page = self.session.get(self.BASE_URL, params=search_params)
            first_page.raise_for_status()
            soup = BeautifulSoup(first_page.text, 'html.parser')

            # 総件数を取得
            total_count_elem = soup.select_one('.SearchMode__result')
            total_count = 0
            if total_count_elem:
                count_text = total_count_elem.text
                import re
                count_match = re.search(r'約([0-9,]+)件', count_text)
                if count_match:
                    total_count = int(count_match.group(1).replace(',', ''))

            # 最初のページの結果を解析
            items = self._parse_search_results(soup)

            # 残りのページを取得（最大5ページまで）
            max_pages = min(5, (total_count + 99) // 100)
            for page in range(2, max_pages + 1):
                search_params['b'] = str((page - 1) * 100 + 1)
                response = self.session.get(self.BASE_URL, params=search_params)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                items.extend(self._parse_search_results(soup))

            return {
                'items': items,
                'total_count': total_count
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
            response = self.session.get(params.get('url'))
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            with open(f"debug_{datetime.now().strftime('%Y%m%d%H%M%S')}.html", "w", encoding="utf-8") as f:
                f.write(soup.prettify())
                # raise ValueError("商品ページの構造が変更されています")
            print("★★開始★★")
            # メタデータからの情報取得

            # 商品基本情報（複数パターン対応）
            detail = {
                'title': '',
                'current_price': '',
                'current_price_in_tax': '',
                'buy_now_price': '',
                'buy_now_price_in_tax': '',
                'start_time': '',
                'end_time': '',
                'auction_id': '',
            }

            # タイトル
            detail['title'] = soup.find('meta', property='og:title')['content'].split(' - ')[0]

            # 商品価格
            price_rows = soup.find_all('div', class_='Price__row')
            for row in price_rows:
                title = row.find('dt', class_='Price__title')
                if not title:
                    continue
                title_text = title.get_text(strip=True)
                value = row.find('dd', class_='Price__value')
                # 現在価格
                if title_text == '現在':
                    if value:
                        detail['current_price'] = value.text.split('円')[0].strip()
                        tax_span = value.find('span', class_='Price__tax')
                        tax = tax_span.text.replace('（税込', '').replace('（税', '').replace('円）', '').strip() if tax_span else '0'
                        detail['current_price_in_tax'] = tax
                # 即決価格
                elif title_text == '即決':
                    if value:
                        detail['buy_now_price'] = value.text.split('円')[0].strip()
                        tax_span = value.find('span', class_='Price__tax')
                        tax = tax_span.text.replace('（税込', '').replace('（税', '').replace('円）', '').strip() if tax_span else '0'
                        detail['buy_now_price_in_tax'] = tax

            # price_rows = soup.find_all('tr', class_='Section__tableRow')
            # for row in price_rows:
            #     title = row.find('th', class_='Section__tableHead')
            #     if not title:
            #         continue
            #     title_text = title.get_text(strip=True)

            #     if(title_text == '出品者'):
            #         detail[]
            #     value = row.find('td', class_='Section__tableData')
            #     if not value:
            #         continue



            print(detail)

            #     'current_price': meta_data['price'],
            #     'currency': meta_data['currency'],
            #     'auction_status': {
            #         'end_time': soup.select_one('time[datetime]')['datetime'],
            #         'bid_count': int(re.search(r'\d+', main_container.select_one('span.BidCount').text).group())
            #     },
            #     'item_details': {
            #         'category': [li.text.strip() for li in soup.select('ol.Breadcrumb li')][1:],
            #         'brand': re.search(r'ブランド: (.+?)<', str(soup)).group(1)
            #     },
            #     'shipping_info': {
            #         'cost': (soup.select_one('dt:contains("送料") + dd').text 
            #                 if soup.select_one('dt:contains("送料")') else '不明'),
            #         'method': [m.text.strip() for m in soup.select('div.ShippingMethod li')]
            #     },
            #     'description': meta_data['description']
            # }

            # # 価格情報のフォールバック
            # if not detail['current_price']:
            #     price_element = soup.select_one('span.Price, div.CurrentPrice')
            #     if price_element:
            #         detail['current_price'] = re.sub(r'\D', '', price_element.text)

            # # 商品詳細テーブル（汎用的な取得方法）
            # for dl in soup.select('dl.ItemInfo'):
            #     key = dl.select_one('dt').text.strip().replace('：', '')
            #     value = dl.select_one('dd').text.strip()
            #     detail['item_details'][key] = value

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
            detail['images'] = {
                'all': sorted_images
            }

            # # JSON-LDデータからの情報抽出
            # script_data = soup.find('script', type='application/ld+json')
            # if script_data:
            #     try:
            #         product_data = json.loads(script_data.string)
            #         detail.update({
            #             'condition': product_data[0].get('offers', {}).get('itemCondition'),
            #             'availability': product_data[0].get('offers', {}).get('availability')
            #         })
            #     except JSONDecodeError:
            #         pass

            return {
                'success': True,
                'data': detail
            }

        except requests.RequestException as e:
            logger.error(f"リクエストエラー: {str(e)}")
            print("error")
            print(e)
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

    def search_categories(self, params):
        """
        カテゴリ検索を実行
        """
        # TODO: カテゴリ検索の実装
        return {
            'categories': []
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
                
                # 価格情報の取得（現在価格と即決価格を区別）
                price_containers = product.select('.Product__price')
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

                seller_elem = product.select_one('.Product__seller')
                end_time_elem = product.select_one('.Product__time')
                bid_count_elem = product.select_one('.Product__bid')
                shipping_elem = product.select_one('.Product__postage')
                condition_elem = product.select_one('.Product__condition')
                location_elem = product.select_one('.Product__location')
                category_elem = product.select_one('.Product__category')
                description_elem = product.select_one('.Product__description')
                payment_elem = product.select_one('.Product__payment')

                if not all([title_elem, url_elem]) or not current_price:
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
                    'payment_methods': payment_elem.text.strip() if payment_elem else None
                }
                items.append(item)
            except Exception as e:
                logger.warning(f"商品情報の抽出に失敗: {str(e)}")
                continue

        return items 