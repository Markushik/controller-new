from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_extension_menu(l10n_text: str):
    menu_builder = InlineKeyboardBuilder()

    menu_builder.row(
        InlineKeyboardButton(
            text=l10n_text,
            callback_data='extension_data',
        )
    )

    return menu_builder.as_markup()
