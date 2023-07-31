from operator import itemgetter

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Group,
    Column,
    Select,
    Button,
    Row
)
from aiogram_dialog.widgets.text import Format, Const

from application.tgbot.dialogs.create_menu.getters import get_subs_for_delete
from application.tgbot.dialogs.delete_menu.handerls import (
    on_click_sub_selected,
    on_click_sub_not_delete
)
from application.tgbot.dialogs.extras.i18n_format import I18NFormat
from application.tgbot.dialogs.main_menu.handler import (
    on_click_get_subs_menu,
    on_click_sub_delete,
)
from application.tgbot.states.states import DeleteMenu

delete_menu = Dialog(
    Window(
        I18NFormat("Catalog-remove"),
        Group(
            Column(
                Select(
                    Format("{item[1]} — {item[2]}"),
                    id="delete_id",
                    item_id_getter=itemgetter(0),
                    items="subs",
                    on_click=on_click_sub_selected,
                    type_factory=int
                ),
            ),
            Button(I18NFormat("Back"), id="back_id", on_click=on_click_get_subs_menu)
        ),
        state=DeleteMenu.DELETE,
        getter=get_subs_for_delete,
    ),
    Window(
        I18NFormat("Are-you-sure"),
        Row(
            Button(Const("✅"), id="confirm_delete_id", on_click=on_click_sub_delete),
            Button(Const("❎"), id="reject_delete_id", on_click=on_click_sub_not_delete),
        ),
        state=DeleteMenu.CHECK_DELETE
    )
)
