from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Row, Button, NumberedPager, Url
from aiogram_dialog.widgets.text import Jinja, Const, ScrollingText

from tgbot.handlers.client import (on_click_get_help, on_click_get_donate, on_click_get_subs, on_click_start_create_sub,
                                   on_click_back_to_main)
from tgbot.states.user import UserSG

VERY_LONG_TEXT = """\
Тестовое сообщение #1

Тестовое сообщение #2
"""

main_menu = Dialog(
    Window(
        Jinja("Hello"),
        Button(Const("🗂 Мои подписки"), id="subs_id", on_click=on_click_get_subs),
        Row(
            Button(Const("💰 Донаты"), id="donate_id", on_click=on_click_get_donate),
            Button(Const("🆘 Поддержка"), id="help_id", on_click=on_click_get_help),
        ),
        state=UserSG.MAIN,
    ),
    Window(
        ScrollingText(
            text=Jinja(VERY_LONG_TEXT),
            id="text_scroll",
            page_size=15,
        ),
        NumberedPager(
            scroll="text_scroll",
        ),
        Button(Const("↩️ Назад"), id="back_id", on_click=on_click_back_to_main),
        state=UserSG.HELP,
    ),
    Window(
        Jinja("🗂️ <b>Каталог активных подписок:</b>\n\n"
              "🤷‍♂️ <b>Кажется</b>, что здесь ничего <b>нет</b>..."),
        Row(
            Button(Const("Добавить"), id="add_id", on_click=on_click_start_create_sub),
            Button(Const("Удалить"), id="remove_id", on_click=on_click_get_help),
        ),
        Button(Const("↩️ Назад"), id="back_id", on_click=on_click_back_to_main),
        state=UserSG.SUBS,
    ),
    Window(
        Jinja("Donate"),
        Row(
            Url(
                Const("☕ 199 ₽"),
                Const('https://github.com/Markushik/controller-new/'),
            ),
            Url(
                Const("🍔 299 ₽"),
                Const('https://github.com/Markushik/controller-new/'),
            ),
            Url(
                Const("🍕 499 ₽"),
                Const('https://github.com/Markushik/controller-new/'),
            ),
        ),
        Button(Const("↩️ Назад"), id="back_id", on_click=on_click_back_to_main),
        state=UserSG.DONATE,
    ),

)
