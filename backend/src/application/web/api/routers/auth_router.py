# src/application/web/api/routers/auth_router.py
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.application.web.api.dependencies import get_auth_service
from src.application.web.api.error_response import ErrorResponse
from src.application.web.api.models.auth_model import Token, LoginModel
from src.domain.exceptions.credentials_error import CredentialsError
from src.domain.exceptions.user_not_found_error import UserNotFoundError
from src.domain.exceptions.invalid_user_input_error import InvalidUserInputError
from src.domain.helpers.convert_entity_to_model import convert_entity_to_model
from src.domain.services.auth_service import AuthService
from src.domain.services.user_service import UserService
from src.infrastructure.authentication.jwt_token import oauth2_scheme
from src.application.web.api.models.user_api_model import UserReadModel
from src.settings import logger


auth_router = APIRouter()

@auth_router.post("/login", response_model=Token, responses={
    400: {"model": ErrorResponse, "description": "Invalid credentials"},
    404: {"model": ErrorResponse, "description": "User not found"},
    500: {"model": ErrorResponse, "description": "Internal server error"}
})
def login(login_model: LoginModel, auth_service: AuthService = Depends(get_auth_service)):
    try:
        logger.info(f"Authenticating user with email: {login_model.email}")
        access_token = auth_service.authenticate_and_generate_token(login_model.email, login_model.password)
        token = Token(access_token=access_token, token_type="bearer")
        return token
    except UserNotFoundError as e:
        error_response = ErrorResponse(
            error_type="UserNotFoundError",
            message="User not found",
            detail=str(e)
        )
        logger.warning(error_response.model_dump_json())
        raise HTTPException(status_code=404, detail=error_response.model_dump_json())
    except InvalidUserInputError as e:
        error_response = ErrorResponse(
            error_type="InvalidUserInputError",
            message="Invalid credentials",
            detail=str(e)
        )
        logger.warning(error_response.model_dump_json())
        raise HTTPException(status_code=400, detail=error_response.model_dump_json())
    except Exception as e:
        error_response = ErrorResponse(
            error_type="InternalServerError",
            message="An unexpected error occurred",
            detail=str(e)
        )
        logger.error(error_response.model_dump_json())
        raise HTTPException(status_code=500, detail=error_response.model_dump_json())


@auth_router.get("/users/me", response_model=UserReadModel, responses={
    401: {"model": ErrorResponse, "description": "Could not validate credentials"},
    404: {"model": ErrorResponse, "description": "User not found"},
    500: {"model": ErrorResponse, "description": "Internal server error"}
})
async def read_users_me(token: str = Depends(oauth2_scheme), auth_service: AuthService = Depends(get_auth_service)):
    try:
        logger.info(f"Fetching user with token: {token}")
        user = auth_service.get_current_user(token)
        user_read_model = convert_entity_to_model(user, UserReadModel)
        return user_read_model
    except CredentialsError as e:
        error_response = ErrorResponse(
            error_type="CredentialsError",
            message="Could not validate credentials",
            detail=str(e)
        )
        logger.warning(error_response.model_dump_json())
        raise HTTPException(status_code=401, detail=error_response.model_dump_json(), headers={"WWW-Authenticate": "Bearer"})
    except UserNotFoundError as e:
        error_response = ErrorResponse(
            error_type="UserNotFoundError",
            message="User not found",
            detail=str(e)
        )
        logger.warning(error_response.model_dump_json())
        raise HTTPException(status_code=404, detail=error_response.model_dump_json())
    except Exception as e:
        error_response = ErrorResponse(
            error_type="InternalServerError",
            message="An unexpected error occurred",
            detail=str(e)
        )
        logger.error(error_response.model_dump_json())
        raise HTTPException(status_code=500, detail=error_response.model_dump_json())
