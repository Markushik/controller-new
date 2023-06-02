from datetime import date
from typing import Any

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode, DialogProtocol
from redis.asyncio import Redis

from tgbot.states.user import UserSG

router = Router()
redis = Redis()


async def service_name_handler(message: Message, dialog: DialogProtocol, manager: DialogManager):
    manager.dialog_data["service"] = message.text
    await manager.switch_to(UserSG.months)


async def months_count_handler(message: Message, dialog: DialogProtocol, manager: DialogManager):
    if message.text.isdigit() and int(message.text) in range(1, 12 + 1):
        manager.dialog_data["months"] = message.text
        await manager.switch_to(UserSG.reminder)
    else:
        await message.answer(text="<b>🚫 Ошибка:</b> Недопустимые символы")


async def on_click_calendar_reminder(query: CallbackQuery, widget: Any, manager: DialogManager,
                                     selected_date: date) -> None:
    manager.dialog_data["reminder"] = (str(date.strftime(selected_date, '%d-%m-%Y')))
    await manager.switch_to(UserSG.check)


async def get_data(dialog_manager: DialogManager, **kwargs):
    return {
        "data": "📩 Проверьте <b>правильность</b> введённых данных:\n\n"
                f"<b>Сервис:</b> <code>{dialog_manager.dialog_data.get('service')}</code>\n"
                f"<b>Длительность:</b> <code>{dialog_manager.dialog_data.get('months')} (мес.)</code>\n"
                f"<b>Оповестить: </b> <code>{dialog_manager.dialog_data.get('reminder')}</code>",
    }


async def start(message: Message, dialog_manager: DialogManager):  # TODO: delete registration start command in __main__
    await dialog_manager.start(UserSG.service, mode=StartMode.RESET_STACK)
