# src/application/web/api/routers/trade_date_router.py
from datetime import date
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Callable

from src.domain.exceptions.data_not_found_error import DataNotFoundError
from src.domain.exceptions.invalid_input_error import InvalidInputError
from src.domain.exceptions.repository_error import RepositoryError
from src.domain.services.trade_date_service import TradeDateService
from src.application.web.api.models.trade_date_model import TradeDateResponse, TradeDateRequest
from src.application.web.api.dependencies import get_trade_date_service
from src.application.web.api.error_response import ErrorResponse
from src.settings import logger

trade_date_router = APIRouter()

@trade_date_router.get("/trade-dates/", response_model=TradeDateResponse, responses={
    400: {"model": ErrorResponse, "description": "Invalid input or data error"},
    404: {"model": ErrorResponse, "description": "Data not found"},
    422: {"model": ErrorResponse, "description": "Validation error for request parameters"},
    500: {"model": ErrorResponse, "description": "Internal server error"}
})
async def get_trade_dates(
    graph_type: str = Query(..., description="Type of the graph data."),
    asset_name: str = Query(..., description="Name of the asset."),
    start_date: date | None = Query(None, description="Start date for the date range filter."),
    end_date: date | None = Query(None, description="End date for the date range filter."),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination."),
    limit: int = Query(100, ge=1, description="Maximum number of records to return."),
    trade_date_service_dependency: Callable[[str], TradeDateService] = Depends(get_trade_date_service)
):
    try:
        request = TradeDateRequest(graph_type=graph_type, asset_name=asset_name, start_date=start_date, end_date=end_date, skip=skip, limit=limit)
        logger.info(f"Fetching trade dates for graph_type: {request.graph_type} asset: {request.asset_name}, start_date: {request.start_date}, end_date: {request.end_date}")

        trade_date_service = trade_date_service_dependency(request.graph_type)
        trade_dates = trade_date_service.fetch_trade_dates(request.asset_name, request.start_date, request.end_date, request.skip, request.limit)

        logger.debug(trade_dates)
        if not trade_dates:
            raise DataNotFoundError("No trade dates found for the given parameters.")

        response_data = [trade_date.trade_date for trade_date in trade_dates]

        logger.info(f"Trade dates fetched: {response_data}")
        return TradeDateResponse(trade_dates=response_data)

    except InvalidInputError as e:
        logger.error(f"Invalid input error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except DataNotFoundError as e:
        logger.error(f"Data not found error: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        logger.error(f"Value error: {e}")
        raise HTTPException(status_code=422, detail=str(e))
    except TypeError as e:
        logger.error(f"Type error: {e}")
        raise HTTPException(status_code=422, detail=str(e))
    except RepositoryError as e:
        logger.error(f"Repository error: {e}")
        raise HTTPException(status_code=500, detail="Error accessing data repository.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
