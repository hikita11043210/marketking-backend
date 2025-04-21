from decimal import Decimal
from django.db import transaction
from ...models.master import ShippingRatesFedex, ShippingRatesDhl, ShippingRatesEconomy, CountriesFedex, CountriesDhl, CountriesEconomy
import numpy as np
import pandas as pd
import logging
import re

# ロガーの設定
logger = logging.getLogger(__name__)

class ImportService:
    """マスターデータのインポート処理を行うサービスクラス"""
    
    def import_fedex_rates(self, file):
        """FedEx送料マスターのインポート処理"""
        try:
            logger.info("FedEx送料マスターのインポート処理を開始します")
            
            # Excelファイルの読み込み（対象シート：SHIPPING RATES（FICP） JP）
            target_sheet = 'SHIPPING RATES（FICP） JP'
            try:
                logger.info(f"シート '{target_sheet}' を読み込み中...")
                df = pd.read_excel(file, sheet_name=target_sheet, header=None)
                logger.info(f"シート '{target_sheet}' の読み込みに成功しました。シェイプ: {df.shape}")
            except ValueError:
                # シート名にかっこが全角と半角で異なる可能性も考慮
                try:
                    logger.info("全角括弧での読み込みに失敗したため、半角括弧で試行します...")
                    df = pd.read_excel(file, sheet_name='SHIPPING RATES(FICP) JP', header=None)
                    logger.info(f"半角括弧シートの読み込みに成功しました。シェイプ: {df.shape}")
                except ValueError as e:
                    logger.error(f"シート読み込みエラー: {str(e)}")
                    # 利用可能なシート名を出力
                    all_sheets = pd.ExcelFile(file).sheet_names
                    logger.info(f"ファイル内の利用可能なシート: {all_sheets}")
                    return {"success": False, "message": f"指定されたシート '{target_sheet}' が見つかりません。利用可能なシート: {all_sheets}"}
            
            # ゾーン情報の取得 (C8〜X8)
            zone_row = 7  # 0-indexedなので8行目は7
            zone_cols = list(range(2, 24))  # C〜X列 (0-indexedなので2〜23)
            zones = {}
            logger.info(f"ゾーン情報の取得を開始します。対象行: {zone_row+1}, 対象列範囲: C-X")
            for col in zone_cols:
                if col < len(df.columns):
                    cell_value = df.iloc[zone_row, col] if zone_row < len(df) else None
                    logger.info(f"セル位置 ({zone_row+1},{chr(65+col)}) の値: {cell_value}")
                    if pd.notna(cell_value):
                        try:
                            # 数値またはテキスト（例: "Zone 1"）の両方に対応
                            if isinstance(cell_value, (int, float, np.integer, np.floating)):
                                zones[col] = str(int(cell_value))  # 整数に変換後、文字列に変換
                                logger.info(f"ゾーン {zones[col]} をカラム {chr(65+col)} に割り当てました")
                            elif isinstance(cell_value, str):
                                # "Zone X"形式から"Zone "部分を削除
                                zone_text = cell_value.strip()
                                if zone_text.lower().startswith('zone'):
                                    # "Zone "または"zone "などを削除
                                    zone_text = re.sub(r'^zone\s+', '', zone_text, flags=re.IGNORECASE)
                                    logger.info(f"文字列 '{cell_value}' から 'Zone ' を削除して '{zone_text}' を抽出しました")
                                
                                # 数字の抽出ではなく、Zone前置詞を削除した値を使用
                                if len(zone_text) > 2:
                                    zone_text = zone_text[:2]  # 2文字に制限
                                zones[col] = zone_text
                                logger.info(f"ゾーン '{zone_text}' をカラム {chr(65+col)} に割り当てました")
                        except (ValueError, TypeError):
                            logger.warning(f"ゾーン値の変換に失敗しました: {cell_value}")
            
            logger.info(f"検出したゾーン情報: {zones}")
            if not zones:
                logger.error("ゾーン情報が検出できませんでした。処理を中止します。")
                return {"success": False, "message": "ゾーン情報が見つかりません。Excelファイルのフォーマットを確認してください。"}
            
            # 一括登録用のデータリスト
            bulk_data = []
            count = 0
            
            # トランザクション開始
            with transaction.atomic():
                # 既存データを全削除
                deleted_count = ShippingRatesFedex.objects.all().delete()[0]
                logger.info(f"既存のFedEx送料データを削除しました: {deleted_count}件")
                
                # 重量と送料のデータ読み込み (B11〜B98 の重量、C11〜X98 の送料)
                weight_start_row = 10  # B11は0-indexedで10行目
                weight_end_row = 97    # B98は0-indexedで97行目
                weight_col = 1         # B列は0-indexedで1
                
                logger.info(f"重量と送料の読み込みを開始します。行範囲: {weight_start_row+1}-{weight_end_row+1}")
                
                # 処理した行とスキップした行をカウント
                processed_rows = 0
                skipped_rows = 0
                
                for row in range(weight_start_row, weight_end_row + 1):
                    if row >= len(df):
                        logger.warning(f"行 {row+1} はデータフレームの範囲外です。処理を終了します。")
                        break
                        
                    weight_val = df.iloc[row, weight_col]
                    logger.debug(f"行 {row+1} の重量値: {weight_val}, 型: {type(weight_val)}")
                    
                    # 重量が数値でない行はスキップ
                    if pd.isna(weight_val) or not isinstance(weight_val, (int, float, np.integer, np.floating)):
                        logger.debug(f"行 {row+1} の重量値をスキップします: {weight_val}")
                        skipped_rows += 1
                        continue
                    
                    processed_rows += 1
                    weight = Decimal(str(weight_val))
                    
                    # 各ゾーンに対する送料を取得
                    for col, zone in zones.items():
                        if col >= len(df.columns):
                            logger.debug(f"列 {chr(65+col)} はデータフレームの範囲外です。")
                            continue
                            
                        rate_val = df.iloc[row, col]
                        logger.debug(f"セル ({row+1},{chr(65+col)}) の送料値: {rate_val}")
                        
                        # 送料が数値でない場合はスキップ
                        if pd.isna(rate_val) or not isinstance(rate_val, (int, float, np.integer, np.floating)):
                            logger.debug(f"セル ({row+1},{chr(65+col)}) の送料値をスキップします: {rate_val}")
                            continue
                        
                        rate = int(rate_val)
                        
                        # モデルインスタンス作成
                        shipping_rate = ShippingRatesFedex(
                            zone=zone,
                            weight=weight,
                            rate=rate
                        )
                        bulk_data.append(shipping_rate)
                        count += 1
                        
                        # 1000件ごとにバルク登録
                        if len(bulk_data) >= 1000:
                            ShippingRatesFedex.objects.bulk_create(bulk_data)
                            logger.info(f"1000件のデータをバルク登録しました。合計: {count}件")
                            bulk_data = []
                
                # 残りのデータをバルク登録
                if bulk_data:
                    ShippingRatesFedex.objects.bulk_create(bulk_data)
                    logger.info(f"残り {len(bulk_data)}件 のデータをバルク登録しました。")
                
                logger.info(f"処理した行数: {processed_rows}, スキップした行数: {skipped_rows}, 登録したデータ数: {count}")
            
            if count == 0:
                return {"success": False, "count": count, "message": "FedEx送料データのインポートに失敗しました。データが0件でした。デバッグログを確認してください。"}
            return {"success": True, "count": count, "message": f"{count}件のFedEx送料データをインポートしました。"}
        
        except Exception as e:
            import traceback
            logger.error(f"FedExインポート処理中に例外が発生しました: {str(e)}")
            logger.error(traceback.format_exc())
            return {"success": False, "message": f"エラーが発生しました: {str(e)}"}
    
    def import_dhl_rates(self, file):
        """DHL送料マスターのインポート処理"""
        try:
            logger.info("DHL送料マスターのインポート処理を開始します")
            
            # Excelファイルの読み込み（対象シート：SHIPPING RATES JP）
            target_sheet = 'SHIPPING RATES JP'
            try:
                logger.info(f"シート '{target_sheet}' を読み込み中...")
                df = pd.read_excel(file, sheet_name=target_sheet, header=None)
                logger.info(f"シート '{target_sheet}' の読み込みに成功しました。シェイプ: {df.shape}")
            except ValueError:
                logger.error(f"シート読み込みエラー")
                # 利用可能なシート名を出力
                all_sheets = pd.ExcelFile(file).sheet_names
                logger.info(f"ファイル内の利用可能なシート: {all_sheets}")
                return {"success": False, "message": f"指定されたシート '{target_sheet}' が見つかりません。利用可能なシート: {all_sheets}"}
            
            # 文書か物品かの識別
            # 例: 1シート目が物品(is_document=False)、2シート目が書類(is_document=True)という想定
            is_document = False
            if 'doc' in file.name.lower() or 'document' in file.name.lower():
                is_document = True
            logger.info(f"処理対象: {'書類' if is_document else '物品'}")
            
            # ゾーン情報の取得 (C6〜M6)
            zone_row = 5  # 0-indexedなので6行目は5
            zone_cols = list(range(2, 13))  # C〜M列 (0-indexedなので2〜12)
            zones = {}
            logger.info(f"ゾーン情報の取得を開始します。対象行: {zone_row+1}, 対象列範囲: C-M")
            for col in zone_cols:
                if col >= len(df.columns):
                    continue
                cell_value = df.iloc[zone_row, col] if zone_row < len(df) else None
                logger.info(f"セル位置 ({zone_row+1},{chr(65+col)}) の値: {cell_value}")
                if pd.notna(cell_value):
                    try:
                        # 数値またはテキスト（例: "Zone 1"）の両方に対応
                        if isinstance(cell_value, (int, float, np.integer, np.floating)):
                            zones[col] = str(int(cell_value))  # 整数に変換後、文字列に変換
                            logger.info(f"ゾーン {zones[col]} をカラム {chr(65+col)} に割り当てました")
                        elif isinstance(cell_value, str):
                            # "Zone X"形式から"Zone "部分を削除
                            zone_text = cell_value.strip()
                            if zone_text.lower().startswith('zone'):
                                # "Zone "または"zone "などを削除
                                zone_text = re.sub(r'^zone\s+', '', zone_text, flags=re.IGNORECASE)
                                logger.info(f"文字列 '{cell_value}' から 'Zone ' を削除して '{zone_text}' を抽出しました")
                            
                            # 数字の抽出ではなく、Zone前置詞を削除した値を使用
                            if len(zone_text) > 2:
                                zone_text = zone_text[:2]  # 2文字に制限
                            zones[col] = zone_text
                            logger.info(f"ゾーン '{zone_text}' をカラム {chr(65+col)} に割り当てました")
                    except (ValueError, TypeError):
                        logger.warning(f"ゾーン値の変換に失敗しました: {cell_value}")
            
            logger.info(f"検出したゾーン情報: {zones}")
            if not zones:
                logger.error("ゾーン情報が検出できませんでした。処理を中止します。")
                return {"success": False, "message": "ゾーン情報が見つかりません。Excelファイルのフォーマットを確認してください。"}
            
            # 一括登録用のデータリスト
            bulk_data = []
            count = 0
            
            # トランザクション開始
            with transaction.atomic():
                # 既存データを一部削除（同じis_document値のデータのみ）
                deleted_count = ShippingRatesDhl.objects.filter(is_document=is_document).delete()[0]
                logger.info(f"既存のDHL送料データを削除しました: {deleted_count}件 (is_document={is_document})")
                
                # 重量と送料のデータ読み込み (B17〜B190 の重量、C17〜M190 の送料)
                weight_start_row = 16  # B17は0-indexedで16行目
                weight_end_row = 189   # B190は0-indexedで189行目
                weight_col = 1         # B列は0-indexedで1
                
                logger.info(f"重量と送料の読み込みを開始します。行範囲: {weight_start_row+1}-{weight_end_row+1}")
                
                # 処理した行とスキップした行をカウント
                processed_rows = 0
                skipped_rows = 0
                
                for row in range(weight_start_row, weight_end_row + 1):
                    # 範囲外になる可能性も考慮
                    if row >= len(df):
                        logger.warning(f"行 {row+1} はデータフレームの範囲外です。処理を終了します。")
                        break
                        
                    weight_val = df.iloc[row, weight_col]
                    logger.debug(f"行 {row+1} の重量値: {weight_val}, 型: {type(weight_val)}")
                    
                    # 重量が数値でない行はスキップ
                    if pd.isna(weight_val) or not isinstance(weight_val, (int, float, np.integer, np.floating)):
                        logger.debug(f"行 {row+1} の重量値をスキップします: {weight_val}")
                        skipped_rows += 1
                        continue
                    
                    processed_rows += 1
                    weight = Decimal(str(weight_val))
                    
                    # 各ゾーンに対する送料を取得
                    for col, zone in zones.items():
                        # 列の範囲チェック
                        if col >= len(df.columns) or col > 12:  # C17〜M190 なので列は最大12(M)まで
                            continue
                            
                        rate_val = df.iloc[row, col]
                        logger.debug(f"セル ({row+1},{chr(65+col)}) の送料値: {rate_val}")
                        
                        # 送料が数値でない場合はスキップ
                        if pd.isna(rate_val) or not isinstance(rate_val, (int, float, np.integer, np.floating)):
                            logger.debug(f"セル ({row+1},{chr(65+col)}) の送料値をスキップします: {rate_val}")
                            continue
                        
                        rate = int(rate_val)
                        
                        # モデルインスタンス作成
                        shipping_rate = ShippingRatesDhl(
                            zone=zone,
                            weight=weight,
                            is_document=is_document,
                            rate=rate
                        )
                        bulk_data.append(shipping_rate)
                        count += 1
                        
                        # 1000件ごとにバルク登録
                        if len(bulk_data) >= 1000:
                            ShippingRatesDhl.objects.bulk_create(bulk_data)
                            logger.info(f"1000件のデータをバルク登録しました。合計: {count}件")
                            bulk_data = []
                
                # 残りのデータをバルク登録
                if bulk_data:
                    ShippingRatesDhl.objects.bulk_create(bulk_data)
                    logger.info(f"残り {len(bulk_data)}件 のデータをバルク登録しました。")
                
                logger.info(f"処理した行数: {processed_rows}, スキップした行数: {skipped_rows}, 登録したデータ数: {count}")
            
            if count == 0:
                return {"success": False, "count": count, "message": "DHL送料データのインポートに失敗しました。データが0件でした。デバッグログを確認してください。"}
            return {"success": True, "count": count, "message": f"{count}件のDHL送料データをインポートしました。"}
        
        except Exception as e:
            import traceback
            logger.error(f"DHLインポート処理中に例外が発生しました: {str(e)}")
            logger.error(traceback.format_exc())
            return {"success": False, "message": f"エラーが発生しました: {str(e)}"}
    
    def import_economy_rates(self, file, country_code=None):
        """
        エコノミー送料マスターのインポート処理
        
        Args:
            file: Excelファイル
            country_code: 国コード（アメリカ、イギリス、ドイツ、オーストラリアのいずれか）
        """
        try:
            # パラメータチェック
            if not country_code:
                return {"success": False, "message": "国コードが指定されていません。"}
            
            # 国コードから国IDを取得
            try:
                country = CountriesEconomy.objects.get(code=country_code)
            except CountriesEconomy.DoesNotExist:
                return {"success": False, "message": f"指定された国コード '{country_code}' は存在しません。"}
            
            # シート名の決定（アメリカの場合は特殊）
            target_sheet = 'SHIPPING RATES JP'
            if country_code.upper() == 'US':
                target_sheet = '48 contiguous states JP'
            
            # Excelファイルの読み込み
            try:
                df = pd.read_excel(file, sheet_name=target_sheet, header=None)
            except ValueError:
                return {"success": False, "message": f"指定されたシート '{target_sheet}' が見つかりません。"}
            
            # 一括登録用のデータリスト
            bulk_data = []
            count = 0
            
            # トランザクション開始
            with transaction.atomic():
                # 既存データを一部削除（同じ国のデータのみ）
                ShippingRatesEconomy.objects.filter(country=country).delete()
                
                # 重量と送料のデータ読み込み
                # 表の左側 (B10〜B42 の重量、C10〜C42 の送料)
                weight_start_row = 9   # B10は0-indexedで9行目
                weight_end_row = 41    # B42は0-indexedで41行目
                weight_col = 1         # B列は0-indexedで1
                rate_col = 2           # C列は0-indexedで2
                
                for row in range(weight_start_row, weight_end_row + 1):
                    # 範囲外になる可能性も考慮
                    if row >= len(df):
                        break
                        
                    weight_val = df.iloc[row, weight_col]
                    
                    # 重量が数値でない行はスキップ
                    if pd.isna(weight_val) or not isinstance(weight_val, (int, float, np.integer, np.floating)):
                        continue
                    
                    weight = Decimal(str(weight_val))
                    rate_val = df.iloc[row, rate_col]
                    
                    # 送料が数値でない場合はスキップ
                    if pd.isna(rate_val) or not isinstance(rate_val, (int, float, np.integer, np.floating)):
                        continue
                    
                    rate = int(rate_val)
                    
                    # モデルインスタンス作成
                    shipping_rate = ShippingRatesEconomy(
                        country=country,
                        weight=weight,
                        rate=rate
                    )
                    bulk_data.append(shipping_rate)
                    count += 1
                
                # 表の右側 (D10〜D42 の重量、E10〜E42 の送料)
                weight_col = 3         # D列は0-indexedで3
                rate_col = 4           # E列は0-indexedで4
                
                for row in range(weight_start_row, weight_end_row + 1):
                    # 範囲外になる可能性も考慮
                    if row >= len(df) or weight_col >= len(df.columns) or rate_col >= len(df.columns):
                        break
                        
                    weight_val = df.iloc[row, weight_col]
                    
                    # 重量が数値でない行または値がない場合はスキップ
                    if pd.isna(weight_val) or not isinstance(weight_val, (int, float, np.integer, np.floating)):
                        continue
                    
                    weight = Decimal(str(weight_val))
                    rate_val = df.iloc[row, rate_col]
                    
                    # 送料が数値でない場合はスキップ
                    if pd.isna(rate_val) or not isinstance(rate_val, (int, float, np.integer, np.floating)):
                        continue
                    
                    rate = int(rate_val)
                    
                    # モデルインスタンス作成
                    shipping_rate = ShippingRatesEconomy(
                        country=country,
                        weight=weight,
                        rate=rate
                    )
                    bulk_data.append(shipping_rate)
                    count += 1
                    
                    # 1000件ごとにバルク登録
                    if len(bulk_data) >= 1000:
                        ShippingRatesEconomy.objects.bulk_create(bulk_data)
                        bulk_data = []
                
                # 残りのデータをバルク登録
                if bulk_data:
                    ShippingRatesEconomy.objects.bulk_create(bulk_data)
            
            return {"success": True, "count": count, "message": f"{count}件のエコノミー送料データをインポートしました。国: {country.name_ja}"}
        
        except Exception as e:
            return {"success": False, "message": f"エラーが発生しました: {str(e)}"}
    
    def import_countries(self, file, carrier_type=None):
        """
        国マスターのインポート処理
        
        Args:
            file: Excelファイル
            carrier_type: キャリアタイプ（'fedex', 'dhl' または 'economy'）
        """
        try:
            logger.info(f"国マスターのインポート処理を開始します。キャリアタイプ: {carrier_type}")
            
            if not carrier_type or carrier_type.lower() not in ['fedex', 'dhl', 'economy']:
                return {"success": False, "message": "キャリアタイプが指定されていないか、不正な値です。'fedex', 'dhl', 'economy'を指定してください。"}
            
            # 読み込むExcelの列範囲を決定
            if carrier_type.lower() == 'fedex':
                logger.info("FedEx用の国マスタ取込設定を使用します")
                # Fedexの場合: C8-C202, B8-B202, D8-D202
                code_col = 2  # C列
                name_ja_col = 0  # A列
                name_en_col = 1  # B列
                zone_col = 3  # D列
                je_ip_col = 4  # E列
                je_ficp_col = 5  # F列
                ji_ip_col = 6  # G列
                ji_ficp_col = 7  # H列
                start_row = 7  # 8行目（0-indexedで7）
                end_row = 201  # 202行目（0-indexedで201）
                model_class = CountriesFedex
            elif carrier_type.lower() == 'dhl':
                logger.info("DHL用の国マスタ取込設定を使用します")
                # DHLの場合: A2-A216, C2-C216, D2-D216, E2-E216, F2-F216, G2-G216, H2-H216, I2-I216
                code_col = 0  # A列
                name_en_col = 1  # B列
                name_ja_col = 2  # C列
                zone_col = 3  # D列
                express_envelope_col = 4  # E列
                express_worldwide_col = 5  # F列
                express_worldwide_1200_col = 6  # G列
                express_worldwide_1030_col = 7  # H列
                express_worldwide_0900_col = 8  # I列
                start_row = 1  # 2行目（0-indexedで1）
                end_row = 215  # 216行目（0-indexedで215）
                model_class = CountriesDhl
            else:  # economy
                logger.info("Economy用の国マスタ取込設定を使用します")
                # Economyの場合: ひとまずFedexと同じ設定で
                code_col = 2  # C列
                name_en_col = 1  # B列
                zone_col = 3  # D列
                start_row = 7  # 8行目（0-indexedで7）
                end_row = 201  # 202行目（0-indexedで201）
                model_class = CountriesEconomy
            
            # Excelファイルの読み込み
            try:
                df = pd.read_excel(file, header=None)
                logger.info(f"Excelファイルの読み込みに成功しました。シェイプ: {df.shape}")
            except Exception as e:
                logger.error(f"Excelファイル読み込みエラー: {str(e)}")
                return {"success": False, "message": f"Excelファイルの読み込みに失敗しました: {str(e)}"}
            
            # 一括登録用のデータリスト
            count_insert = 0
            bulk_data = []
            
            # トランザクション開始
            with transaction.atomic():
                # 既存データを全削除してからインポート
                deleted_count = model_class.objects.all().delete()[0]
                logger.info(f"既存の{carrier_type}国データを全て削除しました: {deleted_count}件")
                
                # 各行を処理
                for row in range(start_row, end_row + 1):
                    if row >= len(df):
                        logger.warning(f"行 {row+1} はデータフレームの範囲外です。処理を終了します。")
                        break
                    
                    # 共通の列を取得（コード、名前、ゾーン）
                    code_val = df.iloc[row, code_col] if code_col < len(df.columns) else None
                    name_ja_val = df.iloc[row, name_ja_col] if name_ja_col < len(df.columns) else None
                    name_en_val = df.iloc[row, name_en_col] if name_en_col < len(df.columns) else None
                    zone_val = df.iloc[row, zone_col] if zone_col < len(df.columns) else None
                    
                    # 値が空の場合はスキップ
                    if pd.isna(code_val) or pd.isna(name_en_val) or pd.isna(name_ja_val):
                        logger.debug(f"行 {row+1} の国コードまたは国名がNullのためスキップします")
                        continue
                    
                    # 文字列型に変換
                    code = str(code_val).strip()
                    name_en = str(name_en_val).strip()
                    name_ja = str(name_ja_val).strip()

                    # 国コードは2文字に制限
                    if len(code) > 2:
                        logger.warning(f"行 {row+1} の国コード '{code}' は2文字を超えています。最初の2文字を使用します。")
                        code = code[:2]
                    
                    # ゾーンの処理
                    zone = None
                    if not pd.isna(zone_val):
                        if isinstance(zone_val, str):
                            # 「Zone 10」「Zone D」などから「Zone 」部分を削除
                            zone_text = zone_val.strip()
                            if zone_text.lower().startswith('zone'):
                                # "Zone "または"zone "などを削除
                                zone_text = re.sub(r'^zone\s+', '', zone_text, flags=re.IGNORECASE)
                                logger.debug(f"ゾーン値 '{zone_val}' から 'Zone ' を削除して '{zone_text}' を抽出しました")
                            
                            # 2文字に制限
                            if len(zone_text) > 2:
                                logger.warning(f"行 {row+1} のゾーン値 '{zone_text}' は2文字を超えています。最初の2文字を使用します。")
                                zone_text = zone_text[:2]
                            
                            zone = zone_text
                            logger.debug(f"ゾーン値 '{zone_val}' から '{zone}' を抽出しました")
                        else:
                            # 数値の場合はそのまま文字列に変換
                            zone = str(zone_val)
                            logger.debug(f"数値 {zone_val} からゾーン '{zone}' を生成しました")
                    
                    # モデルインスタンス作成（キャリアタイプごとに異なる）
                    if carrier_type.lower() == 'fedex':
                        # FedEx固有の列を取得
                        je_ip_val = df.iloc[row, je_ip_col] if je_ip_col < len(df.columns) else None
                        je_ficp_val = df.iloc[row, je_ficp_col] if je_ficp_col < len(df.columns) else None
                        ji_ip_val = df.iloc[row, ji_ip_col] if ji_ip_col < len(df.columns) else None
                        ji_ficp_val = df.iloc[row, ji_ficp_col] if ji_ficp_col < len(df.columns) else None
                        
                        # 値を設定
                        je_ip = str(je_ip_val) if not pd.isna(je_ip_val) else ""
                        je_ficp = str(je_ficp_val) if not pd.isna(je_ficp_val) else ""
                        ji_ip = str(ji_ip_val) if not pd.isna(ji_ip_val) else ""
                        ji_ficp = str(ji_ficp_val) if not pd.isna(ji_ficp_val) else ""
                        
                        # モデルインスタンス作成
                        country = CountriesFedex(
                            code=code,
                            name_en=name_en,
                            name_ja=name_ja,
                            zone=zone or "",
                            je_ip=je_ip[:3],
                            je_ficp=je_ficp[:3],
                            ji_ip=ji_ip[:3],
                            ji_ficp=ji_ficp[:3]
                        )
                    
                    elif carrier_type.lower() == 'dhl':
                        # DHL固有の列を取得
                        express_envelope_val = df.iloc[row, express_envelope_col] if express_envelope_col < len(df.columns) else None
                        express_worldwide_val = df.iloc[row, express_worldwide_col] if express_worldwide_col < len(df.columns) else None
                        express_worldwide_1200_val = df.iloc[row, express_worldwide_1200_col] if express_worldwide_1200_col < len(df.columns) else None
                        express_worldwide_1030_val = df.iloc[row, express_worldwide_1030_col] if express_worldwide_1030_col < len(df.columns) else None
                        express_worldwide_0900_val = df.iloc[row, express_worldwide_0900_col] if express_worldwide_0900_col < len(df.columns) else None
                        
                        # 値を設定
                        express_envelope = str(express_envelope_val) if not pd.isna(express_envelope_val) else ""
                        express_worldwide = str(express_worldwide_val) if not pd.isna(express_worldwide_val) else ""
                        express_worldwide_1200 = str(express_worldwide_1200_val) if not pd.isna(express_worldwide_1200_val) else ""
                        express_worldwide_1030 = str(express_worldwide_1030_val) if not pd.isna(express_worldwide_1030_val) else ""
                        express_worldwide_0900 = str(express_worldwide_0900_val) if not pd.isna(express_worldwide_0900_val) else ""
                        
                        # モデルインスタンス作成
                        country = CountriesDhl(
                            code=code,
                            name_en=name_en,
                            name_ja=name_ja,
                            zone=zone or "",
                            express_envelope=express_envelope[:3],
                            express_worldwide=express_worldwide[:3],
                            express_worldwide_1200=express_worldwide_1200[:3],
                            express_worldwide_1030=express_worldwide_1030[:3],
                            express_worldwide_0900=express_worldwide_0900[:3]
                        )
                    
                    else:  # economy
                        # Economyのモデルインスタンス作成
                        country = CountriesEconomy(
                            code=code,
                            name_en=name_en,
                            name_ja=name_ja,
                            zone=zone or ""
                        )
                    
                    bulk_data.append(country)
                    count_insert += 1
                    
                    # 1000件ごとにバルク登録
                    if len(bulk_data) >= 1000:
                        model_class.objects.bulk_create(bulk_data)
                        logger.info(f"1000件のデータをバルク登録しました。合計: {count_insert}件")
                        bulk_data = []
                
                # 残りのデータをバルク登録
                if bulk_data:
                    model_class.objects.bulk_create(bulk_data)
                    logger.info(f"残り {len(bulk_data)}件 のデータをバルク登録しました。")
            
            logger.info(f"{carrier_type}国データの処理が完了しました。新規: {count_insert}件")
            
            if count_insert == 0:
                return {"success": False, "message": "処理対象のデータがありませんでした。"}
            
            return {
                "success": True, 
                "insert_count": count_insert,
                "message": f"{carrier_type}国データのインポートが完了しました。新規: {count_insert}件"
            }
        
        except Exception as e:
            import traceback
            logger.error(f"国マスターインポート処理中に例外が発生しました: {str(e)}")
            logger.error(traceback.format_exc())
            return {"success": False, "message": f"エラーが発生しました: {str(e)}"} 