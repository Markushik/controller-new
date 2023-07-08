import os
from typing import Dict, Callable, Any, Awaitable, Union

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from fluent.runtime import FluentLocalization, FluentResourceLoader
from sqlalchemy.ext.asyncio import async_sessionmaker

from application.core.config.constants import DEFAULT_LOCALE, LOCALES

from application.tgbot.dialogs.format import I18N_FORMAT_KEY


def make_i18n_middleware(session_pool: async_sessionmaker):
    loader = FluentResourceLoader(os.path.join(
        os.path.dirname(__file__),
        "..",
        "translations",
        "{locale}"
    ))
    l10ns = {
        locale: FluentLocalization(
            [locale, DEFAULT_LOCALE], ["main.ftl"], loader,
        )
        for locale in LOCALES
    }
    return I18nMiddleware(l10ns, DEFAULT_LOCALE, session_pool)


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

        # async with self.session_pool() as session:
        #     try:
        #         request = await session.execute(select(Users).where(Users.user_id == event.from_user.id))
        #         result_all = request.scalar_one()
        #         lang = result_all.language
        #
        #         if lang is None:
        #             raise NoResultFound
        #
        #     except NoResultFound:
        #         await session.merge(
        #             Users(
        #                 user_id=event.from_user.id, user_name=event.from_user.first_name,
        #                 chat_id=event.chat.id, language="ru"
        #             )
        #         )
        #         await session.commit()
        #         lang = event.from_user.language_code
        lang = "ru"
        l10n = self.l10ns[lang]

        data_middleware = dict(zip(["lang", "l10ns", I18N_FORMAT_KEY], [lang, self.l10ns, l10n.format_value]))
        data.update(data_middleware)

        return await handler(event, data)
