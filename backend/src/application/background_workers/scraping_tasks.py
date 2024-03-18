from apscheduler.schedulers.background import BackgroundScheduler
from src.infrastructure.scraping.scraper import scrape_website
from datetime import datetime

def my_job():
    print("Running scheduled task:", datetime.now())
    data = scrape_website()
    # 永続化ロジックをここで呼び出す
    print("Scraped data:", data)

scheduler = BackgroundScheduler()
scheduler.add_job(my_job, 'cron', hour=23, minute=30)  # 毎日23:30に実行

if __name__ == "__main__":
    scheduler.start()
    try:
        # これはスケジューラが中断されないようにするための無限ループです。
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
