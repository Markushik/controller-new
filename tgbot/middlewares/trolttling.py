from typing import Callable, Awaitable, Any, Dict, Optional, MutableMapping

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from cachetools import TTLCache


class ThrottlingMiddleware(BaseMiddleware):
    RATE_LIMIT = 0.7

    def __init__(self, rate_limit: float = RATE_LIMIT) -> None:
        self.cache: MutableMapping[int, None] = TTLCache(maxsize=10_000, ttl=rate_limit)

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        user: Optional[User] = data.get("event_from_user", None)

        if user is not None:
            if user.id in self.cache:
                return

            self.cache[user.id] = None

        return await handler(event, data)
