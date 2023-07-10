import os
from typing import Dict, Callable, Any, Awaitable, Union

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from fluent.runtime import FluentLocalization, FluentResourceLoader

from application.core.config.constants import DEFAULT_LOCALE, LOCALES
from application.tgbot.dialogs.render.format import I18N_FORMAT_KEY


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

        session = data["session"]
        request = await session.get_all_positions(user_id=event.from_user.id)
        result = request.scalar()

        try:
            match result.language:
                case "ru_RU":
                    lang = "ru_RU"
                case "en_GB":
                    lang = "en_GB"
                case _:
                    lang = "ru_RU"
        except AttributeError:
            lang = "ru_RU"

        l10n = self.l10ns[lang]

        data_middleware = dict(zip(["lang", "l10ns", I18N_FORMAT_KEY], [lang, self.l10ns, l10n.format_value]))
        data.update(data_middleware)

        return await handler(event, data)
