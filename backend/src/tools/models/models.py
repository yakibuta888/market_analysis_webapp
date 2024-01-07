# coding: utf-8
from sqlalchemy.types import Integer, Float, String, Boolean, DateTime, Date

from backend.src.infrastructure.database.database import Base
import datetime


# dataframe to sql データ型
dtype = {
    "id": Integer(),
    "month": String(),
    "open": String(),
    "high": String(),
    "low": String(),
    "last": String(),
    "change": Float(),
    "settle": Float(),
    "est_volume": Integer(),
    "prior_day_OI": Integer()
}
