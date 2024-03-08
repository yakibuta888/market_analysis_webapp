from fastapi import APIRouter, Depends, HTTPException
from dataclasses import asdict

from src.settings import logger
from src.application.web.api.dependencies import get_user_service
from src.domain.helpers.convert_entity_to_model import convert_entity_to_model
from src.domain.services.user_service import UserService
from src.domain.entities.user_entity import UserEntity
from src.application.web.api.models.user_api_model import UserCreateModel, UserReadModel
from src.application.web.api.error_response import ErrorResponse
from src.domain.exceptions.user_not_found_error import UserNotFoundError
from src.domain.exceptions.invalid_user_input_error import InvalidUserInputError


user_router = APIRouter()

@user_router.post("/users/", response_model=UserReadModel, responses={
    400: {"model": ErrorResponse, "description": "Invalid input"},
    500: {"model": ErrorResponse, "description": "Internal server error"}
})
def create_user(user_create_model: UserCreateModel, user_service: UserService = Depends(get_user_service)):
    try:
        logger.info(f"Creating user. email: {user_create_model.email}, name: {user_create_model.name}")
        user_entity: UserEntity = user_service.create_user(
            email=user_create_model.email,
            password=user_create_model.password,
            name=user_create_model.name
        )
        user_read_model = convert_entity_to_model(user_entity, UserReadModel)
        logger.info(f"User created: {user_read_model}")
        return user_read_model
    except InvalidUserInputError as e:
        error_response = ErrorResponse(
            error_type="InvalidUserInputError",
            message="Invalid input",
            detail=str(e)
        )
        logger.warning(error_response.model_dump_json())
        raise HTTPException(status_code=400, detail=error_response.model_dump_json())

@user_router.get("/users/{user_id}", response_model=UserReadModel, responses={
    404: {"model": ErrorResponse, "description": "User not found"},
    500: {"model": ErrorResponse, "description": "Internal server error"}
})
def fetch_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    try:
        logger.info(f"Fetching user. id: {user_id}")
        user_entity: UserEntity = user_service.fetch_user_by_id(user_id)
        user_read_model = convert_entity_to_model(user_entity, UserReadModel)
        logger.info(f"User found: {user_read_model}")
        return user_read_model
    except UserNotFoundError as e:
        error_response = ErrorResponse(
            error_type="UserNotFoundError",
            message="User not found",
            detail=str(e)
        )
        logger.warning(error_response.model_dump_json())
        raise HTTPException(status_code=404, detail=error_response.model_dump_json())
