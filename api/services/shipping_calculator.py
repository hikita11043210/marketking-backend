from decimal import Decimal, ROUND_HALF_UP, ROUND_UP
from typing import Dict, Any, Optional

from api.models.master import (
    CountriesFedex,
    CountriesDhl,
    CountriesEconomy,
    ShippingRatesFedex,
    ShippingRatesDhl,
    ShippingRatesEconomy,
)

class ShippingCalculator:
    """送料計算サービス"""
    
    # 容積重量の計算用定数
    FEDEX_DHL_DIVISOR = 5000
    ECONOMY_DIVISOR = 8000
    
    def __init__(self):
        pass
    
    def get_country(self, country_code: str) -> Dict[str, Any]:
        """国コードから国データを取得"""
        try:
            print(f"国コード検索: {country_code}")
            # それぞれのモデルから検索（get()ではなくfilter().first()を使用）
            try:
                fedex_country = CountriesFedex.objects.filter(code=country_code).first()
                print(f"FedEx国データ: {fedex_country}")
            except Exception as e:
                print(f"FedEx国データ検索エラー: {str(e)}")
                fedex_country = None
                
            try:
                dhl_country = CountriesDhl.objects.filter(code=country_code).first()
                print(f"DHL国データ: {dhl_country}")
            except Exception as e:
                print(f"DHL国データ検索エラー: {str(e)}")
                dhl_country = None
                
            try:
                economy_country = CountriesEconomy.objects.filter(code=country_code).first()
                print(f"Economy国データ: {economy_country}")
            except Exception as e:
                print(f"Economy国データ検索エラー: {str(e)}")
                economy_country = None
            
            # すべてのデータがない場合はNoneを返す
            if not fedex_country and not dhl_country and not economy_country:
                print(f"国コード {country_code} のデータがすべて見つかりません")
                return None
                
            # 取得できたデータだけで処理を進める
            name = None
            if fedex_country:
                name = fedex_country.name_ja
            elif dhl_country:
                name = dhl_country.name_ja
            elif economy_country:
                name = economy_country.name_ja
                
            return {
                'fedex': fedex_country,
                'dhl': dhl_country,
                'economy': economy_country,
                'name': name,
                'code': country_code
            }
        except Exception as e:
            import traceback
            print(f"国データ取得エラー: {str(e)}")
            print(traceback.format_exc())
            return None
    
    def calculate_dimensional_weight(self, length: int, width: int, height: int, service_type: str) -> Decimal:
        """容積重量を計算
        
        Args:
            length: 長さ(cm)
            width: 幅(cm)
            height: 高さ(cm)
            service_type: サービスタイプ('fedex', 'dhl', 'economy')
            
        Returns:
            容積重量(kg)
        """
        volume = length * width * height
        
        if service_type in ['fedex', 'dhl']:
            divisor = self.FEDEX_DHL_DIVISOR
        else:  # economy
            divisor = self.ECONOMY_DIVISOR
            
        # 容積重量を計算（小数点第1位まで）
        dimensional_weight = Decimal(str(volume)) / Decimal(str(divisor))
        # 小数点以下が0の場合はそのまま、それ以外は切り上げ
        if dimensional_weight % 1 == 0:
            return dimensional_weight.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
        return dimensional_weight.quantize(Decimal('0.1'), rounding=ROUND_UP)
    
    def get_fedex_rate(self, zone: str, weight: Decimal) -> Optional[int]:
        """FedExの送料を取得"""
        try:
            # 重量以下の最大の重量区分を取得
            shipping_rate = ShippingRatesFedex.objects.filter(
                zone=zone,
                weight__gte=weight
            ).order_by('weight').first()
            
            if not shipping_rate:
                # 最大重量を超える場合は最大の重量区分を使用
                shipping_rate = ShippingRatesFedex.objects.filter(
                    zone=zone
                ).order_by('-weight').first()
                
            if shipping_rate:
                return shipping_rate.rate
                
            return None
        except Exception:
            return None
    
    def get_dhl_rate(self, zone: str, weight: Decimal, is_document: bool) -> Optional[int]:
        """DHLの送料を取得"""
        try:
            # 重量以下の最大の重量区分を取得
            shipping_rate = ShippingRatesDhl.objects.filter(
                zone=zone,
                weight__gte=weight,
                is_document=is_document
            ).order_by('weight').first()
            
            if not shipping_rate:
                # 最大重量を超える場合は最大の重量区分を使用
                shipping_rate = ShippingRatesDhl.objects.filter(
                    zone=zone,
                    is_document=is_document
                ).order_by('-weight').first()
                
            if shipping_rate:
                return shipping_rate.rate
                
            return None
        except Exception:
            return None
    
    def get_economy_rate(self, country: CountriesEconomy, weight: Decimal) -> Optional[int]:
        """Economyの送料を取得"""
        try:
            # 重量以下の最大の重量区分を取得
            shipping_rate = ShippingRatesEconomy.objects.filter(
                country=country,
                weight__gte=weight
            ).order_by('weight').first()
            
            if not shipping_rate:
                # 最大重量を超える場合は最大の重量区分を使用
                shipping_rate = ShippingRatesEconomy.objects.filter(
                    country=country
                ).order_by('-weight').first()
                
            if shipping_rate:
                return shipping_rate.rate
                
            return None
        except Exception:
            return None
    
    def calculate_shipping_cost(self, country_code: str, weight: float, length: int = 0, width: int = 0, 
                               height: int = 0, is_document: bool = False) -> Dict[str, Any]:
        """送料を計算"""
        try:
            # 国データを取得
            country_data = self.get_country(country_code)
            if not country_data:
                return {
                    'success': False,
                    'error': f'国コード {country_code} の情報が見つかりません'
                }
            
            weight_decimal = Decimal(str(weight)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
            print(f"変換後の重量: {weight_decimal}")
            
            # 容積重量の計算（寸法が提供されている場合のみ）
            fedex_dim_weight = dhl_dim_weight = economy_dim_weight = Decimal('0')
            
            if all([length, width, height]):
                fedex_dim_weight = self.calculate_dimensional_weight(length, width, height, 'fedex')
                dhl_dim_weight = fedex_dim_weight  # FedExとDHLは同じ計算式
                economy_dim_weight = self.calculate_dimensional_weight(length, width, height, 'economy')
                print(f"容積重量計算結果 - FedEx/DHL: {fedex_dim_weight}, Economy: {economy_dim_weight}")
            
            # 各配送方法で使用する重量（実重量と容積重量の大きい方）
            fedex_weight = max(weight_decimal, fedex_dim_weight)
            dhl_weight = max(weight_decimal, dhl_dim_weight)
            economy_weight = max(weight_decimal, economy_dim_weight)
            print(f"使用する重量 - FedEx: {fedex_weight}, DHL: {dhl_weight}, Economy: {economy_weight}")
            
            # 各送料を取得
            fedex_rate = None
            dhl_rate = None
            economy_rate = None
            
            if country_data['fedex']:
                fedex_rate = self.get_fedex_rate(country_data['fedex'].zone, fedex_weight)
                print(f"FedEx送料: {fedex_rate}")
            
            if country_data['dhl']:
                dhl_rate = self.get_dhl_rate(country_data['dhl'].zone, dhl_weight, is_document)
                print(f"DHL送料: {dhl_rate}")
            
            if country_data['economy']:
                economy_rate = self.get_economy_rate(country_data['economy'], economy_weight)
                print(f"Economy送料: {economy_rate}")
            
            # レスポンス用のデータ準備
            shipping_rates = {}
            weights_used = {}
            
            if fedex_rate is not None:
                shipping_rates['fedex'] = fedex_rate
                weights_used['fedex'] = float(fedex_weight)
            
            if dhl_rate is not None:
                shipping_rates['dhl'] = dhl_rate
                weights_used['dhl'] = float(dhl_weight)
            
            if economy_rate is not None:
                shipping_rates['economy'] = economy_rate
                weights_used['economy'] = float(economy_weight)
            
            # 推奨サービスを決定（最も安いものを選択）
            recommended_service = None
            min_rate = float('inf')
            
            for service, rate in shipping_rates.items():
                if rate < min_rate:
                    min_rate = rate
                    recommended_service = service
            
            # 少なくとも1つの配送サービスが見つかった場合のみ成功
            if shipping_rates:
                return {
                    'success': True,
                    'message': 'データの取得に成功しました',
                    'data': {
                        'country': {
                            'code': country_code,
                            'name': country_data['name'] or country_code
                        },
                        'physical_weight': float(weight_decimal),
                        'weights_used': weights_used,
                        'shipping_rates': shipping_rates,
                        'recommended_service': recommended_service
                    }
                }
            else:
                return {
                    'success': False,
                    'error': f'送料データが見つかりません。国コード: {country_code}, 重量: {weight}kg'
                }
            
        except Exception as e:
            import traceback
            print(f"送料計算エラー: {str(e)}")
            print(traceback.format_exc())
            return {
                'success': False,
                'error': f'送料計算中にエラーが発生しました: {str(e)}'
            } 