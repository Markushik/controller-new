import os
from typing import Any, Awaitable, Callable, Dict, Union

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from fluent.runtime import FluentLocalization, FluentResourceLoader

from application.tgbot.constants import DEFAULT_LOCALE, LOCALES
from application.infrastructure.database.adapter.adapter import DbAdapter
from application.tgbot.dialogs.extras.i18n_format import I18N_FORMAT_KEY


def make_i18n_middleware():
    loader = FluentResourceLoader(
        os.path.join(
            os.path.dirname(__file__), '..', 'translations', '{locale}'
        )
    )
    l10ns = {
        locale: FluentLocalization(
            [locale, DEFAULT_LOCALE],
            ['main.ftl'],
            loader,
        )
        for locale in LOCALES
    }
    return I18nMiddleware(l10ns, DEFAULT_LOCALE)


class I18nMiddleware(BaseMiddleware):
    def __init__(
        self,
        l10ns: Dict[str, FluentLocalization],
        default_lang: str,
    ):
        super().__init__()
        self.l10ns = l10ns
        self.default_lang = default_lang

    async def __call__(
        self,
        handler: Callable[
            [Union[Message, CallbackQuery], Dict[str, Any]],
            Awaitable[Any],
        ],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any],
    ) -> Any:
        session: DbAdapter = data['session']
        language = await session.get_language(user_id=event.from_user.id)

        language = language or 'ru_RU'
        l10n = self.l10ns[language]

        data['l10n'] = l10n
        data['l10ns'] = self.l10ns
        data[I18N_FORMAT_KEY] = l10n.format_value

        return await handler(event, data)
