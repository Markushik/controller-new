from operator import itemgetter

from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Select,
    Row,
    Button,
    Group, Column
)
from aiogram_dialog.widgets.text import Format, Const

from application.tgbot.dialogs.create_menu.getters import get_subs_for_delete
from application.tgbot.dialogs.edit_menu.getters import get_service_data
from application.tgbot.dialogs.edit_menu.handlers import (
    on_click_set_parameters,
    edit_service_handler,
    on_click_edit_title,
    reject_edit_menu,
    approve_edit_menu
)
from application.tgbot.dialogs.extras.i18n_format import I18NFormat
from application.tgbot.dialogs.main_menu.handler import on_click_get_subs_menu
from application.tgbot.states.states import EditMenu

edit_menu = Dialog(
    Window(
        I18NFormat('Edit-form'),
        Column(
            Select(
                Format('{item[1]} — {item[2]}'),
                id='edit_id',
                item_id_getter=itemgetter(0),
                items='subs',
                on_click=on_click_set_parameters,
                type_factory=int,
            ),
            Button(I18NFormat('Back'), id='back_id', on_click=on_click_get_subs_menu),
        ),
        getter=get_subs_for_delete,
        state=EditMenu.EDIT
    ),
    Window(
        I18NFormat('Set-parameters'),
        Group(
            Row(
                Button(I18NFormat('Title'), id='title_id', on_click=on_click_edit_title),
                Button(I18NFormat('Months'), id='month_id'),
                Button(I18NFormat('Date'), id='date_id'),
            ),
        ),
        state=EditMenu.PARAMETERS
    ),
    Window(
        I18NFormat('Add-service-title'),
        MessageInput(edit_service_handler, content_types=[ContentType.TEXT]),
        state=EditMenu.TITLE
    ),
    Window(
        I18NFormat('Check-title-form'),
        Row(
            Button(
                Const('✅'),
                id='confirm_delete_id',
                on_click=approve_edit_menu
            ),
            Button(
                Const('❎'),
                id='reject_delete_id',
                on_click=reject_edit_menu
            ),
        ),
        getter=get_service_data,
        state=EditMenu.CHECK_TITLE_CHANGE
    ),
)
