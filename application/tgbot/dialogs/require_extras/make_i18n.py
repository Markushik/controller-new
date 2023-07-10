import os

from fluent.runtime import FluentLocalization, FluentResourceLoader

from application.core.config.constants import DEFAULT_LOCALE, LOCALES
from application.tgbot.middlewares.i18n import I18nMiddleware


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
