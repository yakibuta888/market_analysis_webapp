import json
from apscheduler.schedulers.background import BackgroundScheduler

from database import get_asset_id  # 仮の関数; 実際にはDBからアセットIDを取得するロジックを実装する
from src.infrastructure.scraping.cme_scraper import scrape_settlements, scrape_volume_and_open_interest


def schedule_scraping_tasks():
    with open('config/urls.json') as f:
        urls_config = json.load(f)

    for asset, urls in urls_config.items():
        asset_id = get_asset_id(asset)  # アセット名に基づいてDBからIDを取得
        settlements_url = urls["settlements"]
        volume_oi_url = urls["volume_and_open_interest"]

        # Settlementsのスクレイピングタスクをスケジュール
        scheduler.add_job(scrape_settlements, 'cron', [settlements_url, asset_id], hour=23, minute=30)

        # Volume and Open Interestのスクレイピングタスクをスケジュール
        scheduler.add_job(scrape_volume_and_open_interest, 'cron', [volume_oi_url, asset_id], hour=23, minute=45)

scheduler = BackgroundScheduler()
scheduler.start()

schedule_scraping_tasks()

try:
    # スケジューラが中断されないようにする無限ループ
    while True:
        pass
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
