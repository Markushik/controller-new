from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class CallbackExtensionBody(CallbackData, prefix='extension'):
    extension: str
    service: str
    months: int


def get_extension_menu(
        text: str, service: str, months: int,
) -> InlineKeyboardMarkup:
    menu_builder = InlineKeyboardBuilder()

    menu_builder.row(
        InlineKeyboardButton(
            text=text,
            callback_data=CallbackExtensionBody(
                extension='extension', service=service, months=months,
            ).pack()
        )
    )

    return menu_builder.as_markup()
