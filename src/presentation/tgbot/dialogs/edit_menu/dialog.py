from operator import itemgetter

from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Button,
    Column,
    Group,
    Row,
    Select,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Const, Format

from src.presentation.tgbot.states.user import EditMenu
from ..edit_menu.getters import (
    get_service_months_data,
    get_service_reminder_data,
    get_service_title_data,
    get_subs_for_edit,
)
from ..edit_menu.handlers import (
    approve_edit_menu,
    edit_months_handler,
    edit_reminder_handler,
    edit_title_handler,
    on_click_edit_date,
    on_click_edit_months,
    on_click_edit_title,
    on_click_set_parameters,
    reject_edit_menu,
)
from ..extras.calendar import CustomCalendar
from ..extras.i18n_format import I18NFormat
from ..main_menu.handler import on_click_get_subs_menu

edit_menu = Dialog(
    Window(
        I18NFormat('catalog-edit'),
        Column(
            Select(
                Format('{item[1]} — {item[2]}'),
                id='edit_id',
                item_id_getter=itemgetter(0),
                items='subs',
                on_click=on_click_set_parameters,
                type_factory=int,
            ),
            Button(
                I18NFormat('back'), id='back_id', on_click=on_click_get_subs_menu,
            ),
        ),
        getter=get_subs_for_edit,
        state=EditMenu.EDIT,
    ),
    Window(
        I18NFormat('select-parameters'),
        Group(
            Row(
                Button(
                    I18NFormat('title'), id='title_id', on_click=on_click_edit_title,
                ),
                Button(
                    I18NFormat('months'), id='months_id', on_click=on_click_edit_months,
                ),
                Button(
                    I18NFormat('date'), id='date_id', on_click=on_click_edit_date,
                ),
            ),
            SwitchTo(
                I18NFormat('back'), id='back_id', state=EditMenu.EDIT
            ),
        ),
        state=EditMenu.PARAMETERS,
    ),
    Window(
        I18NFormat('add-service-title'),
        MessageInput(func=edit_title_handler, content_types=ContentType.TEXT),
        SwitchTo(
            I18NFormat('back'), id='back_id', state=EditMenu.PARAMETERS
        ),
        state=EditMenu.TITLE,
    ),
    Window(
        I18NFormat('add-service-months'),
        MessageInput(func=edit_months_handler, content_types=ContentType.TEXT),
        SwitchTo(I18NFormat('back'), id='back_id', state=EditMenu.PARAMETERS),
        state=EditMenu.MONTHS,
    ),
    Window(
        I18NFormat('add-calendar-date'),
        Group(
            CustomCalendar(
                id='select_date_id', on_click=edit_reminder_handler
            ),
            SwitchTo(
                I18NFormat('back'), id='back_id', state=EditMenu.PARAMETERS
            ),
        ),
        state=EditMenu.REMINDER,
    ),
    Window(
        I18NFormat('check-title-form'),
        Row(
            Button(
                Const('✅'), id='confirm_delete_id', on_click=approve_edit_menu
            ),
            Button(
                Const('❎'), id='reject_delete_id', on_click=reject_edit_menu
            ),
        ),
        getter=get_service_title_data,
        state=EditMenu.CHECK_TITLE_CHANGE,
    ),
    Window(
        I18NFormat('check-months-form'),
        Row(
            Button(
                Const('✅'), id='confirm_delete_id', on_click=approve_edit_menu
            ),
            Button(
                Const('❎'), id='reject_delete_id', on_click=reject_edit_menu
            ),
        ),
        getter=get_service_months_data,
        state=EditMenu.CHECK_MONTHS_CHANGE,
    ),
    Window(
        I18NFormat('check-reminder-form'),
        Row(
            Button(
                Const('✅'), id='confirm_delete_id', on_click=approve_edit_menu
            ),
            Button(
                Const('❎'), id='reject_delete_id', on_click=reject_edit_menu
            ),
        ),
        getter=get_service_reminder_data,
        state=EditMenu.CHECK_REMINDER_CHANGE,
    ),
)
