def create_email_body(response_data):
    """同期処理の結果からメール本文を作成する"""
    body = "Market King 同期処理結果のお知らせ\n"
    body += "=" * 50 + "\n\n"

    # 同期プロセスの開始・終了時刻
    body += f"【同期処理時間】\n"
    body += f"開始時刻: {response_data.get('start_time', '-')}\n"
    body += f"終了時刻: {response_data.get('end_time', '-')}\n\n"

    # Yahoo Auction
    yahoo_auction_data = response_data.get('yahoo_auction', {})
    if yahoo_auction_data:
        body += "【Yahoo!オークション商品同期】\n"
        if isinstance(yahoo_auction_data, dict) and 'error' not in yahoo_auction_data:
            body += f"対象商品数: {yahoo_auction_data.get('synchronize_target_item', 0)}\n"
            body += f"仕入不可: {yahoo_auction_data.get('count_sold_out_items', 0)}\n\n"
        else:
            body += f"エラーが発生しました: {yahoo_auction_data.get('error', '不明なエラー')}\n\n"

    # Yahoo Free Market
    yahoo_free_market_data = response_data.get('yahoo_free_market', {})
    if yahoo_free_market_data:
        body += "【Yahoo!フリマ商品同期】\n"
        if isinstance(yahoo_free_market_data, dict) and 'error' not in yahoo_free_market_data:
            body += f"対象商品数: {yahoo_free_market_data.get('synchronize_target_item', 0)}\n"
            body += f"仕入不可: {yahoo_free_market_data.get('count_sold_out_items', 0)}\n\n"
        else:
            body += f"エラーが発生しました: {yahoo_free_market_data.get('error', '不明なエラー')}\n\n"

    # eBay
    ebay_data = response_data.get('ebay', {})
    if ebay_data:
        body += "【eBay商品同期】\n"
        if isinstance(ebay_data, dict) and 'error' not in ebay_data:
            body += f"対象商品数: {ebay_data.get('synchronize_target_item', 0)}\n"
            body += f"売却済み商品数: {ebay_data.get('count_sold_out_item', 0)}\n"
            body += f"取消商品数: {ebay_data.get('count_change_status_items', 0)}\n\n"
        else:
            body += f"エラーが発生しました: {ebay_data.get('error', '不明なエラー')}\n\n"

    body += "=" * 50 + "\n"
    body += "※このメールは自動送信されています。"
    
    return body