from typing import Protocol
from datetime import datetime


class AbstractDbAdapter(Protocol):
    async def commit(self):
        raise NotImplementedError

    async def add_user(
            self, user_id: int, user_name: str, chat_id: int
    ):
        raise NotImplementedError

    async def create_subscription(
            self, title: str, months: int, reminder: datetime, service_fk: int
    ):
        raise NotImplementedError

    async def delete_subscription(self, service_id: int):
        raise NotImplementedError

    async def get_user(self, user_id: int):
        raise NotImplementedError

    async def get_service(self, service_id: int):
        raise NotImplementedError

    async def get_services(self, user_id: int):
        raise NotImplementedError

    async def get_quantity_subs(self, user_id: int):
        raise NotImplementedError

    async def get_language(self, user_id: int):
        raise NotImplementedError

    async def update_language(self, user_id: int, language: str):
        raise NotImplementedError

    async def edit_sub_title(self, service_id: int, title: str):
        raise NotImplementedError

    async def edit_sub_months(self, service_id: int, months: int):
        raise NotImplementedError

    async def edit_sub_date(self, service_id: int, reminder: datetime):
        raise NotImplementedError

    async def increment_quantity(self, user_id: int):
        raise NotImplementedError

    async def decrement_quantity(self, user_id: int):
        raise NotImplementedError

    # @abstractmethod
    # async def get_services_by_date(self):
    #     raise NotImplementedError
    #
    # @abstractmethod
    # async def delete_services_by_ids(self, services_ids: list):
    #     raise NotImplementedError
