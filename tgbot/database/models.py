"""
This file contains table assets
"""
from datetime import date

from sqlalchemy import VARCHAR, BigInteger, Integer, Date
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base import BaseModel


class Users(BaseModel):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, nullable=True, primary_key=True)
    user_name: Mapped[str] = mapped_column(VARCHAR(120))
    chat_id: Mapped[int] = mapped_column(BigInteger)


class Services(BaseModel):
    __tablename__ = "services"

    service_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(VARCHAR(30))
    reminder: Mapped[date] = mapped_column(Date)
