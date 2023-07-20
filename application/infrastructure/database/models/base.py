"""
This file creates a base class to define a declarative class
"""

from datetime import datetime

from sqlalchemy import BigInteger, Integer, SmallInteger, ForeignKey, String, DateTime
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, registry
from sqlalchemy.orm import Mapped, mapped_column

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

mapper_registry = registry(metadata=MetaData(naming_convention=convention))


class BaseModel(DeclarativeBase):
    registry = mapper_registry
    metadata = mapper_registry.metadata


class User(BaseModel):
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_name: Mapped[str] = mapped_column(String(length=32))
    chat_id: Mapped[int] = mapped_column(BigInteger)
    language: Mapped[str] = mapped_column(String(length=5), default="ru_RU")
    count_subs: Mapped[int] = mapped_column(SmallInteger, default=0)


class Service(BaseModel):
    __tablename__ = "services"
    __mapper_args__ = {"eager_defaults": True}

    service_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(length=30))
    months: Mapped[int] = mapped_column(SmallInteger)
    reminder: Mapped[datetime] = mapped_column(DateTime)

    service_by_user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"))
