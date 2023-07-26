from datetime import datetime, date

from aiogram.methods import SendMessage
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import (
    DialogProtocol,
    DialogManager,
    StartMode
)
from aiogram_dialog.widgets.kbd import Button

from application.tgbot.states.states import CreateMenu, MainMenu


async def service_name_handler(
        message: Message,
        dialog: DialogProtocol,
        dialog_manager: DialogManager
) -> SendMessage:
    l10n = dialog_manager.middleware_data["l10n"]

    if len(message.text) > 30:
        return await message.answer(l10n.format_value("Error-len-limit"))

    dialog_manager.dialog_data["service"] = message.text
    await dialog_manager.switch_to(CreateMenu.MONTHS)


async def months_count_handler(
        message: Message,
        dialog: DialogProtocol,
        dialog_manager: DialogManager
) -> SendMessage:
    l10n = dialog_manager.middleware_data["l10n"]

    try:
        value = int(message.text)
    except ValueError:
        return await message.answer(l10n.format_value("Error-unsupported-char"))

    if value not in range(1, 12 + 1):
        return await message.answer(l10n.format_value("Error-range-reached"))

    dialog_manager.dialog_data["months"] = int(message.text)
    await dialog_manager.switch_to(CreateMenu.REMINDER)


async def on_click_calendar_reminder(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
        selected_date: date
) -> None:
    dialog_manager.dialog_data["reminder"] = selected_date.isoformat()
    await dialog_manager.switch_to(CreateMenu.CHECK_ADD)


async def on_click_button_confirm(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
) -> SendMessage:
    l10n = dialog_manager.middleware_data["l10n"]
    session = dialog_manager.middleware_data["session"]

    await session.add_subscription(
        title=dialog_manager.dialog_data['service'],
        months=dialog_manager.dialog_data['months'],
        reminder=datetime.fromisoformat(dialog_manager.dialog_data['reminder']),
        service_by_user_id=callback.from_user.id
    )
    await session.increment_count(user_id=dialog_manager.event.from_user.id)
    await session.commit()

    await callback.message.edit_text(l10n.format_value("Approve-sub-add"))
    await dialog_manager.done()
    await dialog_manager.start(MainMenu.CONTROL, mode=StartMode.RESET_STACK)


async def on_click_button_reject(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
) -> SendMessage:
    l10n = dialog_manager.middleware_data["l10n"]

    await callback.message.edit_text(l10n.format_value("Error-sub-add"))
    await dialog_manager.done()
    await dialog_manager.start(MainMenu.CONTROL, mode=StartMode.RESET_STACK)
