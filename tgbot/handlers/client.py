from datetime import date
from typing import Any

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode, DialogProtocol
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.database.models import Services
from tgbot.states.user import SubscriptionSG

router = Router()
redis = Redis()


@router.message(CommandStart())
async def start(message: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(SubscriptionSG.service, mode=StartMode.RESET_STACK)


async def service_name_handler(message: Message, dialog: DialogProtocol, dialog_manager: DialogManager) -> None:
    dialog_manager.dialog_data["service"] = message.text
    await dialog_manager.switch_to(SubscriptionSG.months)


async def months_count_handler(message: Message, dialog: DialogProtocol, dialog_manager: DialogManager) -> None:
    if message.text.isdigit() and int(message.text) in range(1, 12 + 1):
        pass
    else:
        await message.answer(text="<b>🚫 Ошибка:</b> Недопустимые символы")
        return

    dialog_manager.dialog_data["months"] = message.text
    await dialog_manager.switch_to(SubscriptionSG.reminder)


async def on_click_calendar_reminder(query: CallbackQuery, widget: Any, dialog_manager: DialogManager,
                                     selected_date: date) -> None:
    dialog_manager.dialog_data["reminder"] = str(selected_date)  # TODO: fix type
    await dialog_manager.switch_to(SubscriptionSG.check)


async def on_click_button_confirm(query: CallbackQuery, widget: Any, dialog_manager: DialogManager) -> None:
    session: AsyncSession = dialog_manager.middleware_data["session"]

    await session.merge(
        Services(
            title=dialog_manager.dialog_data.get('service'),
            reminder=dialog_manager.dialog_data.get('reminder')
        )
    )
    await session.commit()

    await query.message.answer("<b>✅ Одобрено:</b> Данные успешно записаны")
    await dialog_manager.done()


async def on_click_button_reject(query: CallbackQuery, dialog_manager: DialogManager) -> None:
    await query.message.answer("<b>❎ Отклонено:</b> Данные не записаны")
    await dialog_manager.done()


async def get_data(dialog_manager: DialogManager, **kwargs) -> None:
    return {
        "service": f"<b>Сервис:</b> <code>{dialog_manager.dialog_data.get('service')}</code>\n",
        "months": f"<b>Длительность:</b> <code>{dialog_manager.dialog_data.get('months')} (мес.)</code>\n",
        "reminder": f"<b>Оповестить: </b> <code>{dialog_manager.dialog_data.get('reminder')}</code>"
    }


# async def on_click_get_help(query: CallbackQuery, dialog_manager: DialogManager) -> None:
#     await query.message.edit_text()