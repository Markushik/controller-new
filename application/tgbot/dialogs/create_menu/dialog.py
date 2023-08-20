from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Group, Row
from aiogram_dialog.widgets.text import Const

from application.tgbot.states.user import CreateMenu
from .handlers import (
    months_count_handler,
    on_click_button_confirm,
    on_click_button_reject,
    on_click_calendar_reminder,
    service_name_handler,
)
from ..extras.calendar import CustomCalendar
from ..extras.i18n_format import I18NFormat
from ..main_menu.getters import get_input_service_data
from ..main_menu.handler import on_click_get_subs_menu

create_menu = Dialog(
    Window(
        I18NFormat('Add-service-title'),
        MessageInput(service_name_handler, content_types=[ContentType.TEXT]),
        Button(
            I18NFormat('Back'), id='back_id', on_click=on_click_get_subs_menu
        ),
        state=CreateMenu.TITLE,
    ),
    Window(
        I18NFormat('Add-service-months'),
        MessageInput(months_count_handler, content_types=[ContentType.TEXT]),
        Button(
            I18NFormat('Back'), id='back_id', on_click=on_click_get_subs_menu
        ),
        state=CreateMenu.MONTHS,
    ),
    Window(
        I18NFormat('Add-calendar-date'),
        Group(
            CustomCalendar(
                id='select_date_id',
                on_click=on_click_calendar_reminder,
            ),
            Button(
                I18NFormat('Back'),
                id='back_id',
                on_click=on_click_get_subs_menu,
            ),
        ),
        state=CreateMenu.REMINDER,
    ),
    Window(
        I18NFormat('Check-form'),
        Row(
            Button(
                Const('✅'),
                id='confirm_add_id',
                on_click=on_click_button_confirm,
            ),
            Button(
                Const('❎'), id='reject_add_id', on_click=on_click_button_reject
            ),
        ),
        state=CreateMenu.CHECK_ADD,
    ),
    getter=get_input_service_data,
)
