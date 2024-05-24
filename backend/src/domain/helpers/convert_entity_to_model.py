#src/domain/helpers/convert_entity_to_model.py
from dataclasses import asdict
from typing import Any, Type
from pydantic import BaseModel
from src.domain.helpers.dataclass import DataClassBase


def convert_entity_to_model(entity: DataClassBase, model: Type[BaseModel]) -> BaseModel:
    entity_dict = asdict(entity)

    # カスタム型の変換
    to_model_dict = {}
    for field, value in entity_dict.items():
        normalise_field = field.lstrip('_')
        if isinstance(value, dict) and len(value) == 1:
            to_model_dict[normalise_field] = next(iter(value.values()))
        else:
            to_model_dict[normalise_field] = value
    return model(**to_model_dict)
