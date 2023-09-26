from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from .base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_name: Mapped[str] = mapped_column(String(length=32))
    chat_id: Mapped[int] = mapped_column(BigInteger)
    language: Mapped[str] = mapped_column(String(length=5), default='ru_RU')
    count_subs: Mapped[int] = mapped_column(SmallInteger, default=0)

    def __repr__(self) -> str:
        return f'User:{self.user_id}:{self.user_name}'


class Service(BaseModel):
    __tablename__ = 'services'

    service_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    service_fk: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.user_id'))
    title: Mapped[str] = mapped_column(String(length=30))
    months: Mapped[int] = mapped_column(SmallInteger)
    reminder: Mapped[datetime] = mapped_column(DateTime)

    user = relationship(argument='User', lazy='joined', innerjoin=True)

    def __repr__(self) -> str:
        return f'Service:{self.service_id}:{self.title}:{self.reminder}'


class CommonService(BaseModel):
    __tablename__ = 'common_services'

    title: Mapped[str] = mapped_column(String(length=255), primary_key=True)

    def __repr__(self) -> str:
        return f'CommonService:{self.title}'
