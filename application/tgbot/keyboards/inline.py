from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_extension_menu(text: str):
    menu_builder = InlineKeyboardBuilder()

    menu_builder.row(
        InlineKeyboardButton(
            text=text,
            callback_data='extension_data',
        )
    )

    return menu_builder.as_markup()
