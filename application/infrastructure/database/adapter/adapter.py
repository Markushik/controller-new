from datetime import datetime

from sqlalchemy import (
    select,
    delete,
    insert
)
from sqlalchemy.ext.asyncio import AsyncSession

from application.infrastructure.database.models import User, Service


class DbAdapter:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self) -> None:
        return await self.session.commit()

    async def get_user(self, user_id: int) -> None:
        return await self.session.get(User, user_id)

    async def get_service(self, service_id: int) -> None:
        return await self.session.scalar(
            select(Service).where(Service.service_id == service_id)
        )

    async def get_services(self, user_id: int) -> None:
        return (
            await self.session.scalars(
                select(Service).where(Service.service_fk == user_id)
            )
        ).all()

    async def get_user_count_subs(self, user_id: int) -> None:
        return await self.session.scalar(
            select(User.count_subs).where(User.user_id == user_id)
        )

    async def get_user_language(self, user_id: int) -> None:
        return await self.session.scalar(
            select(User.language).where(User.user_id == user_id)
        )

    async def add_user(
            self, user_id: int, user_name: str, chat_id: int
    ) -> None:
        return await self.session.execute(
            insert(User).values(
                user_id=user_id, user_name=user_name, chat_id=chat_id
            )
        )

    async def create_subscription(
            self, title: str, months: int, reminder: datetime, service_fk: int
    ) -> None:
        return await self.session.execute(
            insert(Service).values(
                title=title,
                months=months,
                reminder=reminder,
                service_fk=service_fk,
            )
        )

    async def edit_title_subscription(
            self, service_id: int, title: str
    ) -> None:
        return await self.session.merge(
            Service(service_id=service_id, title=title)
        )

    async def edit_months_subscription(
            self, service_id: int, months: int
    ) -> None:
        return await self.session.merge(
            Service(service_id=service_id, months=months)
        )

    async def edit_date_subscription(
            self, service_id: int, reminder: datetime
    ) -> None:
        return await self.session.merge(
            Service(service_id=service_id, reminder=reminder)
        )

    async def update_language(self, user_id: int, language: str) -> None:
        return await self.session.merge(
            User(user_id=user_id, language=language)
        )

    async def delete_subscription(self, service_id: int) -> None:
        return await self.session.execute(
            delete(Service).where(Service.service_id == service_id)
        )

    async def increment_count(self, user_id: int) -> None:
        return await self.session.merge(
            User(user_id=user_id, count_subs=User.count_subs + 1)
        )

    async def decrement_count(self, user_id: int) -> None:
        return await self.session.merge(
            User(user_id=user_id, count_subs=User.count_subs - 1)
        )
