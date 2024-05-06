# src/application/web/api/routers/asset_router.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from src.settings import logger
from src.application.web.api.dependencies import get_asset_service
from src.application.web.api.models.asset_model import AssetModel
from src.application.web.api.error_response import ErrorResponse
from src.domain.exceptions.asset_not_found_error import AssetNotFoundError
from src.domain.helpers.convert_entity_to_model import convert_entity_to_model
from src.domain.services.asset_service import AssetService
from src.infrastructure.mysql.asset_repository_mysql import AssetRepositoryMysql


asset_router = APIRouter()

@asset_router.get("/assets", response_model=list[AssetModel], tags=["assets"], responses={
    404: {"model": ErrorResponse, "description": "Assets not found"},
    500: {"model": ErrorResponse, "description": "Internal server error"}
})
def fetch_assets(asset_service: AssetService = Depends(get_asset_service)):
    try:
        logger.info("Fetching assets")
        assets = asset_service.fetch_all()
        asset_model_list = [convert_entity_to_model(asset, AssetModel) for asset in assets]
        logger.info(f"Assets found: {asset_model_list}")
        return asset_model_list
    except AssetNotFoundError as e:
        error_response = ErrorResponse(
            error_type="AssetNotFound",
            message="Asset not found",
            detail=str(e)
        )
        logger.error(error_response.model_dump_json())
        raise HTTPException(status_code=404, detail=error_response.model_dump_json())
    except Exception as e:
        error_response = ErrorResponse(
            error_type="InternalServerError",
            message="Internal server error",
            detail=str(e)
        )
        logger.error(error_response.model_dump_json())
        raise HTTPException(status_code=500, detail=error_response.model_dump_json())
