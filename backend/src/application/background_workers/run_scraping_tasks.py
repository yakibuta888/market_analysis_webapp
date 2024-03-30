# src/application/background_workers/run_scraping_tasks.py
from src.domain.services.asset_service import AssetService
from src.domain.services.settlement_service import SettlementService
from src.domain.services.volume_oi_service import VolumeOIService
from src.infrastructure.mysql.asset_repository_mysql import AssetRepositoryMysql
from src.infrastructure.mysql.settlement_repository_mysql import SettlementRepositoryMysql
from src.infrastructure.mysql.volume_oi_repository_mysql import VolumeOIRepositoryMysql
from src.infrastructure.database.database import db_session
from src.infrastructure.scraping import cme_scraper
from src.settings import logger


def run_settlements_scraping_task():
    logger.info("Running settlements scraping task")
    asset_service = AssetService(AssetRepositoryMysql(db_session()))
    settlement_service = SettlementService(SettlementRepositoryMysql(db_session()))
    cme_scraper.scrape_settlements(asset_service, settlement_service)


def run_volume_oi_scraping_task():
    logger.info("Running volume and open interest scraping task")
    asset_service = AssetService(AssetRepositoryMysql(db_session()))
    volume_oi_service = VolumeOIService(VolumeOIRepositoryMysql(db_session()))
    cme_scraper.scrape_volume_and_open_interest(asset_service, volume_oi_service)


# コマンドライン引数を使って、実行するタスクを指定
def main():
    import sys

    if len(sys.argv) > 1:
        task_name = sys.argv[1]
        if task_name == "settlement":
            run_settlements_scraping_task()
        elif task_name == "volume_oi":
            run_volume_oi_scraping_task()
        else:
            print(f"Unknown task: {task_name}")
    else:
        print("No task specified.")


if __name__ == "__main__":
    main()
