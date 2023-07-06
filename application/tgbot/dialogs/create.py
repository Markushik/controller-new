from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Row, Calendar
from aiogram_dialog.widgets.text import Const

from application.tgbot.dialogs.format import I18NFormat
from application.tgbot.handlers.client import (service_name_handler, months_count_handler, on_click_calendar_reminder,
                                               get_input_service_data, on_click_button_confirm, on_click_button_reject,
                                               on_click_get_subs_menu)
from application.tgbot.states.user import SubscriptionSG

dialog = Dialog(
    Window(
        I18NFormat("Add-service-title"),
        MessageInput(service_name_handler, content_types=[ContentType.TEXT]),
        Button(I18NFormat("Back"), id="back_id", on_click=on_click_get_subs_menu),
        state=SubscriptionSG.SERVICE,
    ),
    Window(
        I18NFormat("Add-service-months"),
        MessageInput(months_count_handler, content_types=[ContentType.TEXT]),
        state=SubscriptionSG.MONTHS,
    ),
    Window(
        I18NFormat("Add-calendar-date"),
        Calendar(
            id="select_date_id",
            on_click=on_click_calendar_reminder,
        ),
        state=SubscriptionSG.REMINDER,
    ),
    Window(
        I18NFormat("Check-form"),
        Row(
            Button(Const("✅"), id="confirm_add_id", on_click=on_click_button_confirm),
            Button(Const("❎"), id="reject_add_id", on_click=on_click_button_reject),
        ),
        state=SubscriptionSG.CHECK,
    ),
    getter=get_input_service_data
)
