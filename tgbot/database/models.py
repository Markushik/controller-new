"""
This file contains table assets
"""

from datetime import datetime

from sqlalchemy import VARCHAR, BigInteger, Integer, SmallInteger, ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Users(BaseModel):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_name: Mapped[str] = mapped_column(VARCHAR(length=120))
    chat_id: Mapped[int] = mapped_column(BigInteger)


class Services(BaseModel):
    __tablename__ = "services"

    service_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(VARCHAR(length=30))
    months: Mapped[int] = mapped_column(SmallInteger)
    reminder: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))

    service_by_user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"))

# class Schedulers(BaseModel):
#     __tablename__ = "schedulers"
#
#     ...
