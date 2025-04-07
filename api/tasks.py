from celery import shared_task, group
from api.services.synchronize.yahoo_auction import SynchronizeYahooAuction
from api.services.synchronize.ebay import Status as EbayStatus
from api.services.synchronize.yahoo_free_market import SynchronizeYahooFreeMarket
import logging

logger = logging.getLogger(__name__)

@shared_task
def sync_yahoo_auction():
    try:
        yahoo_auction = SynchronizeYahooAuction()
        result = yahoo_auction.synchronize()
        return {'status': 'success', 'data': result}
    except Exception as e:
        logger.error(f"Yahoo Auction同期中にエラーが発生しました: {str(e)}")
        return {'status': 'error', 'error': str(e)}

@shared_task
def sync_yahoo_free_market():
    try:
        yahoo_free_market = SynchronizeYahooFreeMarket()
        result = yahoo_free_market.synchronize()
        return {'status': 'success', 'data': result}
    except Exception as e:
        logger.error(f"Yahoo Free Market同期中にエラーが発生しました: {str(e)}")
        return {'status': 'error', 'error': str(e)}

@shared_task
def sync_ebay():
    try:
        ebay = EbayStatus()
        result = ebay.synchronize()
        return {'status': 'success', 'data': result}
    except Exception as e:
        logger.error(f"eBay同期中にエラーが発生しました: {str(e)}")
        return {'status': 'error', 'error': str(e)}

@shared_task
def sync_all():
    try:
        logger.info("同期処理を開始します")
        
        # 全ての同期タスクを並行して実行
        job = group([
            sync_yahoo_auction.s(),
            sync_yahoo_free_market.s(),
            sync_ebay.s()
        ])
        
        result = job.apply_async()
        task_results = result.get(timeout=600)
        
        # 結果をログに出力
        for i, task_name in enumerate(['Yahoo Auction', 'Yahoo Free Market', 'eBay']):
            status = task_results[i].get('status')
            if status == 'success':
                logger.info(f"{task_name}: 同期成功")
            else:
                logger.error(f"{task_name}: 同期失敗 - {task_results[i].get('error')}")
        
        return {'status': 'success', 'message': '全ての同期処理が完了しました'}
        
    except Exception as e:
        logger.error(f"同期処理中にエラーが発生しました: {str(e)}")
        return {'status': 'error', 'error': str(e)} 