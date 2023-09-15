from operator import itemgetter

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Column, Group, Row, Select
from aiogram_dialog.widgets.text import Const, Format

from application.tgbot.dialogs.main_menu.handler import (
    on_click_get_subs_menu,
    on_click_sub_delete,
)
from application.tgbot.states.user import DeleteMenu
from ..extras.i18n_format import I18NFormat
from .getters import get_subs_for_delete
from .handlers import on_click_sub_not_delete, on_click_sub_selected

delete_menu = Dialog(
    Window(
        I18NFormat('catalog-remove'),
        Group(
            Column(
                Select(
                    Format('{item[1]} — {item[2]}'),
                    id='delete_id',
                    item_id_getter=itemgetter(0),
                    items='subs',
                    on_click=on_click_sub_selected,
                    type_factory=int,
                ),
            ),
            Button(
                I18NFormat('back'), id='back_id', on_click=on_click_get_subs_menu,
            ),
        ),
        getter=get_subs_for_delete,
        state=DeleteMenu.DELETE,
    ),
    Window(
        I18NFormat('conformation'),
        Row(
            Button(
                Const('✅'), id='confirm_delete_id', on_click=on_click_sub_delete,
            ),
            Button(
                Const('❎'), id='reject_delete_id', on_click=on_click_sub_not_delete,
            ),
        ),
        state=DeleteMenu.CHECK_DELETE,
    ),
)
