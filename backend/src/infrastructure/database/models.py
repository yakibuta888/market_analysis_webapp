# src/infrastructure/database/models.py

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(128), unique=True, index=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    name = Column(String(64), nullable=False)

class Asset(Base):
    __tablename__ = 'assets'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)

    settlements = relationship("Settlement", back_populates="asset")
    volume_oi_data = relationship("VolumeOI", back_populates="asset")

class Settlement(Base):
    __tablename__ = 'settlements'

    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey('assets.id'), nullable=False)
    trade_date = Column(Date, nullable=False)
    month = Column(String(16), nullable=False)
    open = Column(String(16))
    high = Column(String(16))
    low = Column(String(16))
    last = Column(String(16))
    change = Column(Float(precision=2))
    settle = Column(Float(precision=2), nullable=True)
    est_volume = Column(Integer, nullable=False)
    prior_day_oi = Column(Integer, nullable=False)
    is_final = Column(Boolean, nullable=False)

    asset = relationship("Asset", back_populates="settlements")

    __table_args__ = (UniqueConstraint('asset_id', 'trade_date', 'month', name='_asset_date_month_uc'),)

class VolumeOI(Base):
    __tablename__ = 'volume_oi'

    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey('assets.id'), nullable=False)
    trade_date = Column(Date, nullable=False)
    month = Column(String(16), nullable=False)
    globex = Column(Integer)
    open_outcry = Column(Integer)
    clear_port = Column(Integer)
    total_volume = Column(Integer, nullable=False)
    block_trades = Column(Integer)
    efp = Column(Integer)
    efr = Column(Integer)
    tas = Column(Integer)
    deliveries = Column(Integer)
    at_close = Column(Integer, nullable=False)
    change = Column(Integer)
    is_final = Column(Boolean, nullable=False)

    asset = relationship("Asset", back_populates="volume_oi_data")

    __table_args__ = (UniqueConstraint('asset_id', 'trade_date', 'month', name='_asset_date_month_uc'),)
