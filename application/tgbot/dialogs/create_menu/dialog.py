from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const

from application.tgbot.dialogs._extras.calendar import CustomCalendar
from application.tgbot.dialogs.create_menu.handlers import (
    months_count_handler,
    service_name_handler,
    on_click_calendar_reminder,
    on_click_button_confirm,
    on_click_button_reject
)
from application.tgbot.dialogs._extras.i18n_format import I18NFormat
from application.tgbot.dialogs.main_menu.getters import get_input_service_data
from application.tgbot.dialogs.main_menu.handler import on_click_get_subs_menu
from application.tgbot.states.user import SubscriptionMenu

create_menu = Dialog(
    Window(
        I18NFormat("Add-service-title"),
        MessageInput(service_name_handler, content_types=[ContentType.TEXT]),
        Button(I18NFormat("Back"), id="back_id", on_click=on_click_get_subs_menu),
        state=SubscriptionMenu.service,
    ),
    Window(
        I18NFormat("Add-service-months"),
        MessageInput(months_count_handler, content_types=[ContentType.TEXT]),
        state=SubscriptionMenu.months,
    ),
    Window(
        I18NFormat("Add-calendar-date"),
        CustomCalendar(
            id="select_date_id",
            on_click=on_click_calendar_reminder,
        ),
        state=SubscriptionMenu.reminder,
    ),
    Window(
        I18NFormat("Check-form"),
        Row(
            Button(Const("✅"), id="confirm_add_id", on_click=on_click_button_confirm),
            Button(Const("❎"), id="reject_add_id", on_click=on_click_button_reject),
        ),
        state=SubscriptionMenu.result,
    ),
    getter=get_input_service_data
)
