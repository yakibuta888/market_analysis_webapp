# src/application/web/api/routers/futures_data_router.py

from datetime import date, datetime
from fastapi import APIRouter, HTTPException, Depends, Query

from src.domain.exceptions.dataframe_validation_error import DataFrameValidationError
from src.domain.exceptions.invalid_input_error import InvalidInputError
from src.domain.exceptions.repository_error import RepositoryError
from src.domain.services.futures_data_service import FuturesDataService
from src.domain.logics.convert_dataframe import dataframe_to_json, to_year_month_format
from src.application.web.api.models.futures_data_model import FuturesDataResponse, FuturesDataRequest
from src.application.web.api.dependencies import get_futures_data_service
from src.application.web.api.error_response import ErrorResponse
from src.settings import logger

futures_data_router = APIRouter()

@futures_data_router.get("/futures-data/{asset_name}", response_model=FuturesDataResponse, responses={
    400: {"model": ErrorResponse, "description": "Invalid input or data error"},
    404: {"model": ErrorResponse, "description": "Data not found"},
    422: {"model": ErrorResponse, "description": "Validation error for request parameters"},
    500: {"model": ErrorResponse, "description": "Internal server error"}
})
async def get_futures_data(
    asset_name: str,
    trade_dates: list[date] = Query(..., description="取引日（複数指定可）"),
    futures_data_service: FuturesDataService = Depends(get_futures_data_service)
):
    try:
        request = FuturesDataRequest(asset_name=asset_name, trade_dates=trade_dates)
        logger.info(f"Fetching futures data for asset: {request.asset_name}, trade_dates: {request.trade_dates}")

        df = futures_data_service.make_dataframe(request.asset_name, request.trade_dates)

        if df.empty:
            logger.error("No data found for the given parameters.")
            raise HTTPException(status_code=404, detail="No data found for the given parameters.")

        df = futures_data_service.add_settlement_spread(df)
        df = to_year_month_format(df, 'month')
        response_data = dataframe_to_json(df)

        logger.info(f"Futures data fetched: {response_data['data']}")
        return FuturesDataResponse(data=response_data['data'])

    except InvalidInputError as e:
        logger.error(f"Invalid input error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except DataFrameValidationError as e:
        logger.error(f"Data frame validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        logger.error(f"Value error: {e}")
        raise HTTPException(status_code=422, detail=str(e))
    except RepositoryError as e:
        logger.error(f"Repository error: {e}")
        raise HTTPException(status_code=500, detail="Error accessing data repository.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
