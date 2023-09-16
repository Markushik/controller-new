from datetime import date, datetime

import markupsafe
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, DialogProtocol, StartMode
from aiogram_dialog.widgets.kbd import Button

from application.tgbot.states.user import CreateMenu, MainMenu


async def add_title_handler(
        message: Message, protocol: DialogProtocol, dialog_manager: DialogManager
) -> Message:
    l10n = dialog_manager.middleware_data['l10n']

    if len(message.text) > 30:
        return await message.answer(l10n.format_value('error-len-limit'))

    dialog_manager.dialog_data['service'] = markupsafe.escape(message.text)
    await dialog_manager.switch_to(state=CreateMenu.MONTHS)


async def add_months_handler(
        message: Message, protocol: DialogProtocol, dialog_manager: DialogManager
) -> Message:
    l10n = dialog_manager.middleware_data['l10n']

    try:
        value = int(message.text)
    except ValueError:
        return await message.answer(
            l10n.format_value('error-unsupported-char')
        )

    if value not in range(1, 12 + 1):
        return await message.answer(l10n.format_value('error-range-reached'))

    dialog_manager.dialog_data['months'] = int(message.text)
    await dialog_manager.switch_to(state=CreateMenu.REMINDER)


async def on_click_select_date(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
        selected_date: date,
) -> None:
    dialog_manager.dialog_data['reminder'] = selected_date.isoformat()
    await dialog_manager.switch_to(state=CreateMenu.CHECK_ADD)


async def on_click_confirm_data(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    l10n = dialog_manager.middleware_data['l10n']
    session = dialog_manager.middleware_data['session']

    await session.create_subscription(
        title=dialog_manager.dialog_data['service'],
        months=dialog_manager.dialog_data['months'],
        reminder=datetime.fromisoformat(dialog_manager.dialog_data['reminder']),
        service_fk=callback.from_user.id,
    )
    await session.increment_quantity(user_id=dialog_manager.event.from_user.id)
    await session.commit()

    await callback.message.edit_text(l10n.format_value('approve-sub-add'))
    await dialog_manager.done()
    await dialog_manager.start(state=MainMenu.CONTROL, mode=StartMode.RESET_STACK)


async def on_click_reject_data(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    l10n = dialog_manager.middleware_data['l10n']

    await callback.message.edit_text(l10n.format_value('error-sub-add'))
    await dialog_manager.done()
    await dialog_manager.start(state=MainMenu.CONTROL, mode=StartMode.RESET_STACK)
