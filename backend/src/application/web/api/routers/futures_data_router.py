# src/application/web/api/routers/futures_data_router.py

from datetime import date, datetime
from fastapi import APIRouter, HTTPException, Depends

from src.domain.services.futures_data_service import FuturesDataService
from src.domain.logics.convert_dataframe import dataframe_to_json, to_year_month_format
from src.application.web.api.models.futures_data_model import FuturesDataResponse, FuturesDataRequest
from src.application.web.api.error_response import ErrorResponse
from src.settings import logger

futures_data_router = APIRouter()

@futures_data_router.get("/futures-data/{asset_name}", response_model=FuturesDataResponse, responses={
    400: {"model": ErrorResponse, "description": "Invalid input or data error"},
    500: {"model": ErrorResponse, "description": "Internal server error"}
})
async def get_futures_data(
    request: FuturesDataRequest = Depends(),
    futures_data_service: FuturesDataService = Depends()
):
    try:
        logger.info(f"Fetching futures data for asset: {request.asset_name}, trade_dates: {request.trade_dates}")

        df = futures_data_service.make_dataframe(request.asset_name, request.trade_dates)
        df = futures_data_service.add_settlement_spread(df)

        df = to_year_month_format(df, 'month')
        response_data = dataframe_to_json(df)

        return FuturesDataResponse(data=response_data['data'])




    except Exception as e:
        logger.error(f"Error fetching futures data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
