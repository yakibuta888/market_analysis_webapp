
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ...domain.entities.user_entity import UserEntity
from ...domain.services.user_service import UserService
from ...domain.repositories.user_repository import UserRepository

router = APIRouter()

# 依存性注入の例
def get_user_service():
    user_repository = UserRepository()
    return UserService(user_repository)

@router.post("/users/", response_model=UserEntity)
def create_user(user: UserEntity, service: UserService = Depends(get_user_service)):
    # ユーザー作成ロジック
    return service.create_user(user)

@router.get("/users/{user_id}", response_model=UserEntity)
def read_user(user_id: int, service: UserService = Depends(get_user_service)):
    # 特定のユーザーを取得するロジック
    return service.get_user(user_id)
