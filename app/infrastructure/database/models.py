"""
This file contains table assets
"""

from datetime import datetime

from sqlalchemy import VARCHAR, BigInteger, Integer, SmallInteger, ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Users(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_name: Mapped[str] = mapped_column(VARCHAR(length=32))
    chat_id: Mapped[int] = mapped_column(BigInteger)
    language: Mapped[str] = mapped_column(VARCHAR(length=2), nullable=True)
    count_subs: Mapped[int] = mapped_column(SmallInteger)


class Services(Base):
    __tablename__ = "services"

    service_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(VARCHAR(length=30))
    months: Mapped[int] = mapped_column(SmallInteger)
    reminder: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))

    service_by_user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"))
