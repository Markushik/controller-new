from typing import Dict, Callable, Any, Awaitable, Union

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from fluent.runtime import FluentLocalization
from sqlalchemy import select
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.infrastructure.database.models import Users
from app.tgbot.dialogs.format import I18N_FORMAT_KEY


class I18nMiddleware(BaseMiddleware):
    def __init__(
            self,
            l10ns: Dict[str, FluentLocalization],
            default_lang: str,
            session_pool: async_sessionmaker
    ):
        super().__init__()
        self.l10ns = l10ns
        self.default_lang = default_lang
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[
                [Union[Message, CallbackQuery], Dict[str, Any]],
                Awaitable[Any],
            ],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any],
    ) -> Any:

        try:
            async with self.session_pool() as session:
                request = await session.execute(
                    select(Users)
                    .where(Users.user_id == event.from_user.id)
                )
                result_all = request.one()
                lang = result_all.Users.language
        except InvalidRequestError:
            lang = "ru"

        l10n = self.l10ns[lang]

        data["locales"] = l10n.locales
        data[I18N_FORMAT_KEY] = l10n.format_value

        return await handler(event, data)
