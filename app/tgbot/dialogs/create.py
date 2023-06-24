from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Row, Calendar
from aiogram_dialog.widgets.text import Jinja, Format, Const

from app.tgbot.handlers.client import (service_name_handler, months_count_handler, on_click_calendar_reminder,
                                       get_input_service_data, on_click_button_confirm, on_click_button_reject,
                                       on_click_get_subs_menu)
from app.tgbot.states.user import SubscriptionSG

dialog = Dialog(
    Window(
        Jinja("Как называется <b>сервис</b> на который Вы <b>подписались</b>?\n\n"
              "<b>Пример:</b> <code>Tinkoff Premium</code>"),
        MessageInput(service_name_handler, content_types=[ContentType.TEXT]),
        Button(Const("↩️ Назад"), id="back_id", on_click=on_click_get_subs_menu),
        state=SubscriptionSG.SERVICE,
    ),
    Window(
        Jinja("Сколько <b>месяцев</b> будет действовать подписка?\n\n"
              "<b>Пример:</b> <code>12 (мес.)</code>"),
        MessageInput(months_count_handler, content_types=[ContentType.TEXT]),
        state=SubscriptionSG.MONTHS,
    ),
    Window(
        Jinja("В какую <b>дату</b> оповестить о <b>ближайшем списании</b>?"),
        Calendar(
            id="select_date_id",
            on_click=on_click_calendar_reminder,
        ),
        state=SubscriptionSG.REMINDER,
    ),
    Window(
        Format("📩 Проверьте <b>правильность</b> введённых данных:\n\n"
               "{service}{months}{reminder}"),
        Row(
            Button(Const("✅"), id="confirm_add_id", on_click=on_click_button_confirm),
            Button(Const("❎"), id="reject_add_id", on_click=on_click_button_reject),
        ),
        state=SubscriptionSG.CHECK,
    ),
    getter=get_input_service_data
)
