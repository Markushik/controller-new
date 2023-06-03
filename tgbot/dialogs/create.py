from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Calendar, Button, Row
from aiogram_dialog.widgets.text import Jinja, Format, Const

from tgbot.handlers.client import service_name_handler, months_count_handler, on_click_calendar_reminder, get_data, \
    on_click_button_confirm, on_click_button_reject
from tgbot.states.user import UserSG

dialog = Dialog(
    Window(
        Jinja("— Как называется <b>сервис</b> на который вы <b>подписались</b>?\n\n"
              "<b>Пример:</b> <code>Tinkoff Premium</code>"),
        MessageInput(service_name_handler, content_types=[ContentType.TEXT]),
        state=UserSG.service,
    ),
    Window(
        Jinja("— Сколько <b>месяцев</b> будет действовать подписка?\n\n"
              "<b>Пример:</b> <code>12 (мес.)</code>"),
        MessageInput(months_count_handler, content_types=[ContentType.TEXT]),
        state=UserSG.months,
    ),
    Window(
        Jinja("— В какую <b>дату</b> оповестить о <b>ближайшем списании</b>?"),
        Calendar(
            id="select_date_on_calendar",
            on_click=on_click_calendar_reminder,
        ),
        state=UserSG.reminder,
    ),
    Window(
        Format("📩 Проверьте <b>правильность</b> введённых данных:\n\n"
               "{service}{months}{reminder}"),
        Row(
            Button(Const("✅"), id="confirm_id", on_click=on_click_button_confirm),
            Button(Const("❎"), id="reject_id", on_click=on_click_button_reject),
        ),
        state=UserSG.check,
    ),
    getter=get_data
)
