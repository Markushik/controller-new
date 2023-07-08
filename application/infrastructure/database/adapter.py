from datetime import datetime

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from application.infrastructure.database.models import User, Service


class DbAdapter:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self):
        return await self.session.commit()

    async def get_user(self, user_id: int):
        return await self.session.get(User, user_id)

    async def get_services(self, user_id: int):
        return await self.session.execute(select(Service).where(Service.service_by_user_id == user_id))

    async def get_all_positions(self, user_id: int):
        return await self.session.execute(select(User).where(User.user_id == user_id))

    async def add_user(self, user_id: int, user_name: str, chat_id: int, language: str, count_subs: int):
        return self.session.add(
            User(
                user_id=user_id, user_name=user_name, chat_id=chat_id,
                language=language, count_subs=count_subs
            )
        )

    async def add_subscription(self, title: str, months: str, reminder: datetime, service_by_user_id: int):
        return self.session.add(
            Service(
                title=title, months=months,
                reminder=reminder, service_by_user_id=service_by_user_id
            )
        )

    async def delete_subscription(self, service_id: int):
        return await self.session.execute(delete(Service).where(Service.service_id == service_id))

    async def increment_count(self, user_id: int):
        return await self.session.merge(User(user_id=user_id, count_subs=User.count_subs + 1))

    async def decrement_count(self, user_id: int):
        return await self.session.merge(User(user_id=user_id, count_subs=User.count_subs - 1))

    async def update_language(self, user_id: int, language: str):
        return await self.session.merge(User(user_id=user_id, language=language))
