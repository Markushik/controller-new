from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Group, Row
from aiogram_dialog.widgets.text import Const

from application.tgbot.states.user import CreateMenu
from .handlers import (
    add_months_handler,
    on_click_confirm_data,
    on_click_reject_data,
    on_click_select_date,
    add_title_handler,
)
from ..extras.calendar import CustomCalendar
from ..extras.i18n_format import I18NFormat
from ..main_menu.getters import get_input_service_data
from ..main_menu.handler import on_click_get_subs_menu

create_menu = Dialog(
    Window(
        I18NFormat('add-service-title'),
        MessageInput(func=add_title_handler, content_types=ContentType.TEXT),
        Button(
            I18NFormat('back'), id='back_id', on_click=on_click_get_subs_menu
        ),
        state=CreateMenu.TITLE,
    ),
    Window(
        I18NFormat('add-service-months'),
        MessageInput(func=add_months_handler, content_types=ContentType.TEXT),
        Button(
            I18NFormat('back'), id='back_id', on_click=on_click_get_subs_menu
        ),
        state=CreateMenu.MONTHS,
    ),
    Window(
        I18NFormat('add-calendar-date'),
        Group(
            CustomCalendar(
                id='select_date_id', on_click=on_click_select_date
            ),
            Button(
                I18NFormat('back'), id='back_id', on_click=on_click_get_subs_menu,
            ),
        ),
        state=CreateMenu.REMINDER,
    ),
    Window(
        I18NFormat('check-form'),
        Row(
            Button(
                Const('✅'), id='confirm_add_id', on_click=on_click_confirm_data,
            ),
            Button(
                Const('❎'), id='reject_add_id', on_click=on_click_reject_data
            ),
        ),
        state=CreateMenu.CHECK_ADD,
    ),
    getter=get_input_service_data,
)
