#src/domain/helpers/convert_entity_to_model.py
from dataclasses import asdict
from typing import Any, Type
from pydantic import BaseModel
from src.domain.helpers.dataclass import DataClassBase


def convert_entity_to_model(entity: DataClassBase, model: Type[BaseModel]) -> BaseModel:
    entity_dict = asdict(entity)

    # カスタム型の変換
    for field, value in entity_dict.items():
        if isinstance(value, dict) and len(value) == 1:
            entity_dict[field] = next(iter(value.values()))
    return model(**entity_dict)
