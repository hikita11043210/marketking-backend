from django.test import TestCase
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from api.services.yahoo_auction import YahooAuctionService

class TestYahooAuctionService(TestCase):
    def setUp(self):
        self.service = YahooAuctionService()
        self.test_url = 'https://page.auctions.yahoo.co.jp/jp/auction/test123'
        
        # 正常系のHTMLレスポンスを用意
        self.valid_html = """
        <html>
            <head>
                <meta property="og:title" content="テスト商品 - ヤフオク!" />
            </head>
            <body>
                <div class="Price__row">
                    <dt class="Price__title">現在</dt>
                    <dd class="Price__value">1,000円<span class="Price__tax">（税込1,100円）</span></dd>
                </div>
                <div class="Price__row">
                    <dt class="Price__title">即決</dt>
                    <dd class="Price__value">2,000円<span class="Price__tax">（税込2,200円）</span></dd>
                </div>
                <table>
                    <tr class="Section__tableRow">
                        <th class="Section__tableHead">オークションID</th>
                        <td class="Section__tableData">test123</td>
                    </tr>
                    <tr class="Section__tableRow">
                        <th class="Section__tableHead">カテゴリ</th>
                        <td class="Section__tableData">
                            <a>カテゴリ1</a>
                            <a>カテゴリ2</a>
                        </td>
                    </tr>
                    <tr class="Section__tableRow">
                        <th class="Section__tableHead">状態</th>
                        <td class="Section__tableData"><a>新品</a></td>
                    </tr>
                    <tr class="Section__tableRow">
                        <th class="Section__tableHead">開始日時</th>
                        <td class="Section__tableData">2024-02-01 12:00</td>
                    </tr>
                    <tr class="Section__tableRow">
                        <th class="Section__tableHead">終了日時</th>
                        <td class="Section__tableData">2024-02-08 12:00</td>
                    </tr>
                </table>
                <div class="ProductImage">
                    <li class="ProductImage__image">
                        <img src="https://auctions.c.yimg.jp/images/1.jpg" />
                    </li>
                    <li class="ProductImage__image">
                        <img src="https://auctions.c.yimg.jp/images/2.jpg" />
                    </li>
                </div>
            </body>
        </html>
        """

    @patch('requests.Session.get')
    def test_get_item_detail_success(self, mock_get):
        """正常系: 商品詳細の取得が成功するケース"""
        # モックレスポンスの設定
        mock_response = MagicMock()
        mock_response.text = self.valid_html
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # テスト実行
        result = self.service.get_item_detail({'url': self.test_url})

        # アサーション
        self.assertIn('data', result)
        data = result['data']
        self.assertEqual(data['title'], 'テスト商品')
        self.assertEqual(data['current_price'], '1,000')
        self.assertEqual(data['current_price_in_tax'], '1,100')
        self.assertEqual(data['buy_now_price'], '2,000')
        self.assertEqual(data['buy_now_price_in_tax'], '2,200')
        self.assertEqual(data['auction_id'], 'test123')
        self.assertEqual(data['categories'], ['カテゴリ1', 'カテゴリ2'])
        self.assertEqual(data['condition'], '新品')
        self.assertEqual(data['start_time'], '2024-02-01 12:00')
        self.assertEqual(data['end_time'], '2024-02-08 12:00')
        self.assertEqual(len(data['images']['url']), 2)

    @patch('requests.Session.get')
    def test_get_item_detail_missing_fields(self, mock_get):
        """異常系: 必須フィールドが欠けているケース"""
        # 一部フィールドが欠けたHTMLを用意
        incomplete_html = """
        <html>
            <head>
                <meta property="og:title" content="テスト商品 - ヤフオク!" />
            </head>
            <body>
                <div class="Price__row">
                    <dt class="Price__title">現在</dt>
                    <dd class="Price__value">1,000円</dd>
                </div>
            </body>
        </html>
        """
        
        mock_response = MagicMock()
        mock_response.text = incomplete_html
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = self.service.get_item_detail({'url': self.test_url})
        
        # 欠けているフィールドがmissing_keysに含まれていることを確認
        self.assertIn('missing_keys', result)
        self.assertTrue(len(result['missing_keys']) > 0)

    @patch('requests.Session.get')
    def test_get_item_detail_network_error(self, mock_get):
        """異常系: ネットワークエラーのケース"""
        mock_get.side_effect = requests.RequestException("Network error")
        
        result = self.service.get_item_detail({'url': self.test_url})
        
        self.assertFalse(result.get('success', True))
        self.assertIn('error', result)

    @patch('requests.Session.get')
    def test_get_item_detail_invalid_html(self, mock_get):
        """異常系: 無効なHTMLが返されるケース"""
        mock_response = MagicMock()
        mock_response.text = "Invalid HTML"
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = self.service.get_item_detail({'url': self.test_url})
        
        self.assertIn('missing_keys', result)
        self.assertTrue(len(result['missing_keys']) > 0) 