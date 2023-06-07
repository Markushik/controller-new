"""
This file contains table assets
"""
from typing import Optional

from sqlalchemy import VARCHAR, BigInteger, Integer, SmallInteger
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base import BaseModel


class Users(BaseModel):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)
    user_name: Mapped[Optional[str]] = mapped_column(VARCHAR(120))
    chat_id: Mapped[Optional[int]] = mapped_column(BigInteger)


class Services(BaseModel):
    __tablename__ = "services"

    service_id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, nullable=False)
    title: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    months: Mapped[Optional[int]] = mapped_column(SmallInteger)
    reminder: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
