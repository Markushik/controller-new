from operator import itemgetter

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Group,
    Column,
    Select,
    Button,
    Row
)
from aiogram_dialog.widgets.text import Format

from application.tgbot.dialogs.change_menu.handlers import on_click_sub_change
from application.tgbot.dialogs.create_menu.getters import get_subs_for_delete
from application.tgbot.dialogs.extras.i18n_format import I18NFormat
from application.tgbot.dialogs.main_menu.handler import (
    on_click_get_subs_menu,
)
from application.tgbot.states.states import ChangeMenu

change_menu = Dialog(
    Window(
        I18NFormat("Catalog-change"),
        Group(
            Column(
                Select(
                    Format("{item[1]} — {item[2]}"),
                    id="change_id",
                    item_id_getter=itemgetter(0),
                    items="subs",
                    on_click=on_click_sub_change,
                ),
            ),
        ),
        Button(I18NFormat("Back"), id="back_id", on_click=on_click_get_subs_menu),
        state=ChangeMenu.CHANGE,
        getter=get_subs_for_delete,
    ),
    Window(
        I18NFormat("Set par"),
        Group(
            Row(
                Button(I18NFormat("Title"), id="title_id"),
                Button(I18NFormat("Months"), id="months_id"),
                Button(I18NFormat("Date"), id="date_id"),
            ),
            Button(I18NFormat("Back"), id="back_id", on_click=on_click_get_subs_menu),
        ),
        state=ChangeMenu.PARAMETERS,
    ),
)
