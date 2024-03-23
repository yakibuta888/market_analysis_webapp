from src.domain.services.asset_service import AssetService
from src.infrastructure.mysql.asset_repository_mysql import AssetRepositoryMysql
from src.infrastructure.database.database import db_session
from src.infrastructure.scraping import cme_scraper


if __name__ == "__main__":
    asset_service = AssetService(AssetRepositoryMysql(db_session))
    cme_scraper.scrape_settlements(asset_service)
