from datetime import date, datetime

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode, DialogProtocol
from aiogram_dialog.widgets.kbd import Button
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.database.models import Services, Users
from tgbot.states.user import SubscriptionSG, UserSG

router = Router()


@router.message(CommandStart())
async def command_start(message: Message, dialog_manager: DialogManager) -> None:
    session: AsyncSession = dialog_manager.middleware_data["session"]

    await session.merge(
        Users(
            user_id=message.from_user.id,
            user_name=message.from_user.first_name,
            chat_id=message.chat.id
        )
    )
    await session.commit()


    await dialog_manager.start(UserSG.MAIN, mode=StartMode.RESET_STACK)


async def on_click_start_create_sub(message: Message, dialog: DialogProtocol, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(SubscriptionSG.SERVICE, mode=StartMode.RESET_STACK)


async def service_name_handler(message: Message, dialog: DialogProtocol, dialog_manager: DialogManager) -> None:
    dialog_manager.dialog_data["service"] = message.text
    await dialog_manager.switch_to(SubscriptionSG.MONTHS)


async def months_count_handler(message: Message, dialog: DialogProtocol, dialog_manager: DialogManager) -> None:
    if message.text.isdigit() and int(message.text) in range(1, 12 + 1):
        pass
    else:
        await message.answer(text="<b>🚫 Ошибка:</b> Недопустимые символы")
        return

    dialog_manager.dialog_data["months"] = int(message.text)
    await dialog_manager.switch_to(SubscriptionSG.REMINDER)


async def on_click_calendar_reminder(query: CallbackQuery, button: Button, dialog_manager: DialogManager,
                                     selected_date: date) -> None:
    dialog_manager.dialog_data["reminder"] = selected_date.isoformat()
    await dialog_manager.switch_to(SubscriptionSG.CHECK)


async def on_click_button_confirm(query: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    session: AsyncSession = dialog_manager.middleware_data["session"]
    await session.merge(
        Services(
            title=dialog_manager.dialog_data.get('service'),
            months=dialog_manager.dialog_data.get('months'),
            reminder=datetime.fromisoformat(dialog_manager.dialog_data.get('reminder')),
            service_by_user_id=query.from_user.id
        )
    )
    await session.commit()

    await query.message.edit_text("<b>✅ Одобрено:</b> Данные успешно записаны")
    await dialog_manager.done()
    await dialog_manager.start(UserSG.SUBS, mode=StartMode.RESET_STACK)


async def on_click_button_reject(query: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    await query.message.edit_text("<b>❎ Отклонено:</b> Данные не записаны")
    await dialog_manager.done()
    await dialog_manager.start(UserSG.SUBS, mode=StartMode.RESET_STACK)


async def get_data(dialog_manager: DialogManager, **kwargs) -> None:
    return {
        "service": f"<b>Сервис:</b> <code>{dialog_manager.dialog_data.get('service')}</code>\n",
        "months": f"<b>Длительность:</b> <code>{dialog_manager.dialog_data.get('months')} (мес.)</code>\n",
        "reminder": f"<b>Оповестить: </b> <code>{dialog_manager.dialog_data.get('reminder')}</code>"
    }


async def on_click_get_help(query: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(UserSG.HELP, mode=StartMode.RESET_STACK)


async def on_click_get_subs(query: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(UserSG.SUBS, mode=StartMode.RESET_STACK)


async def on_click_get_donate(query: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(UserSG.DONATE, mode=StartMode.RESET_STACK)


async def on_click_back_to_main(query: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(UserSG.MAIN, mode=StartMode.RESET_STACK)
