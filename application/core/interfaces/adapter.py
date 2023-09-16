from abc import ABC, abstractmethod
from datetime import datetime


class AbstractDbAdapter(ABC):
    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def add_user(
            self, user_id: int, user_name: str, chat_id: int
    ):
        raise NotImplementedError

    @abstractmethod
    async def create_subscription(
            self, title: str, months: int, reminder: datetime, service_fk: int
    ):
        raise NotImplementedError

    @abstractmethod
    async def delete_subscription(self, service_id: int):
        raise NotImplementedError

    @abstractmethod
    async def get_user(self, user_id: int):
        raise NotImplementedError

    @abstractmethod
    async def get_service(self, service_id: int):
        raise NotImplementedError

    @abstractmethod
    async def get_services(self, user_id: int):
        raise NotImplementedError

    @abstractmethod
    async def get_quantity_subs(self, user_id: int):
        raise NotImplementedError

    @abstractmethod
    async def get_language(self, user_id: int):
        raise NotImplementedError

    @abstractmethod
    async def update_language(self, user_id: int, language: str):
        raise NotImplementedError

    @abstractmethod
    async def edit_sub_title(self, service_id: int, title: str):
        raise NotImplementedError

    @abstractmethod
    async def edit_sub_months(self, service_id: int, months: int):
        raise NotImplementedError

    @abstractmethod
    async def edit_sub_date(self, service_id: int, reminder: datetime):
        raise NotImplementedError

    @abstractmethod
    async def increment_quantity(self, user_id: int):
        raise NotImplementedError

    @abstractmethod
    async def decrement_quantity(self, user_id: int):
        raise NotImplementedError
