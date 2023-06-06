from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Row, Button
from aiogram_dialog.widgets.text import Jinja, Const, Format

from tgbot.handlers.client import on_click_get_help, on_click_get_donate, on_click_get_subs
from tgbot.states.user import UserSG

main_menu = Dialog(
    Window(
        Jinja("Hello"),
        Button(Const("🗂 Мои подписки"), id="subs_id", on_click=on_click_get_subs),
        Row(
            Button(Const("💰 Донаты"), id="donate_id", on_click=on_click_get_donate),
            Button(Const("🆘 Поддержка"), id="help_id", on_click=on_click_get_help),
        ),
        state=UserSG.main,
    ),
    Window(
        Jinja("Help"),  # TODO: create nice menu how to use with MultiGroup
        state=UserSG.help,
    ),
    Window(
        Jinja("Subs"),  # TODO: add button "add" and "delete"
        state=UserSG.subs,
    ),
    Window(
        Jinja("Donate"),  # TODO: add button
        state=UserSG.donate,
    )
)
