# src/application/web/api/models/asset_model.py
from pydantic import BaseModel, ConfigDict


class AssetModel(BaseModel):
    id: int
    name: str
