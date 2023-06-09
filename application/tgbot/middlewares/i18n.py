import os
from typing import Dict, Callable, Any, Awaitable, Union

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from fluent.runtime import FluentLocalization, FluentResourceLoader

from application.core.config.constants import DEFAULT_LOCALE, LOCALES
from application.infrastructure.database.repositories.adapter import Repo
from application.tgbot.dialogs._extras.i18n_format import I18N_FORMAT_KEY


def make_i18n_middleware():
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
        session: Repo = data["session"]
        user = await session.get_user_language(user_id=event.from_user.id)

        lang = "ru_RU"

        if user and user.language == "en_GB":
            lang = "en_GB"

        l10n = self.l10ns[lang]
        data_middleware = dict(zip(["l10n", "l10ns", I18N_FORMAT_KEY], [l10n, self.l10ns, l10n.format_value]))
        data.update(data_middleware)

        return await handler(event, data)
