from datetime import date, datetime

import markupsafe
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, DialogProtocol, StartMode
from aiogram_dialog.widgets.kbd import Button

from application.tgbot.states.user import EditMenu, MainMenu


async def on_click_get_edit_menu(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(state=EditMenu.EDIT, mode=StartMode.RESET_STACK)


async def on_click_set_parameters(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
    item_id: int,
) -> None:
    dialog_manager.dialog_data['service_id'] = item_id
    await dialog_manager.switch_to(state=EditMenu.PARAMETERS)


async def on_click_edit_title(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(state=EditMenu.TITLE)


async def on_click_edit_months(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(state=EditMenu.MONTHS)


async def on_click_edit_date(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(state=EditMenu.REMINDER)


async def edit_title_handler(
    message: Message, protocol: DialogProtocol, dialog_manager: DialogManager
) -> Message:
    l10n = dialog_manager.middleware_data['l10n']
    session = dialog_manager.middleware_data['session']

    if len(message.text) > 30:
        return await message.answer(l10n.format_value('Error-len-limit'))

    service_id = dialog_manager.dialog_data['service_id']
    service = await session.get_service(service_id=service_id)

    dialog_manager.dialog_data['service_old_title'] = service.title
    dialog_manager.dialog_data['service_new_title'] = markupsafe.escape(
        message.text
    )

    await dialog_manager.switch_to(state=EditMenu.CHECK_TITLE_CHANGE)


async def edit_months_handler(
    message: Message, protocol: DialogProtocol, dialog_manager: DialogManager
) -> Message:
    l10n = dialog_manager.middleware_data['l10n']
    session = dialog_manager.middleware_data['session']

    try:
        value = int(message.text)
    except ValueError:
        return await message.answer(
            l10n.format_value('Error-unsupported-char')
        )

    if value not in range(1, 12 + 1):
        return await message.answer(l10n.format_value('Error-range-reached'))

    service_id = dialog_manager.dialog_data['service_id']
    service = await session.get_service(service_id=service_id)

    dialog_manager.dialog_data['service_old_months'] = service.months
    dialog_manager.dialog_data['service_new_months'] = int(message.text)

    await dialog_manager.switch_to(state=EditMenu.CHECK_MONTHS_CHANGE)


async def edit_reminder_handler(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
    selected_date: date,
) -> None:
    session = dialog_manager.middleware_data['session']

    service_id = dialog_manager.dialog_data['service_id']
    service = await session.get_service(service_id=service_id)

    dialog_manager.dialog_data[
        'service_old_reminder'
    ] = service.reminder.date().isoformat()
    dialog_manager.dialog_data[
        'service_new_reminder'
    ] = selected_date.isoformat()

    await dialog_manager.switch_to(state=EditMenu.CHECK_REMINDER_CHANGE)


async def reject_edit_menu(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
) -> None:
    l10n = dialog_manager.middleware_data['l10n']

    await callback.message.edit_text(l10n.format_value('Reject-sub-edit'))
    await dialog_manager.done()
    await dialog_manager.start(state=EditMenu.EDIT, mode=StartMode.RESET_STACK)


async def approve_edit_menu(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    l10n = dialog_manager.middleware_data['l10n']
    session = dialog_manager.middleware_data['session']

    if dialog_manager.dialog_data.get('service_new_title'):
        await session.edit_title_subscription(
            service_id=dialog_manager.dialog_data['service_id'],
            title=dialog_manager.dialog_data['service_new_title'],
        )
    if dialog_manager.dialog_data.get('service_new_months'):
        await session.edit_months_subscription(
            service_id=dialog_manager.dialog_data['service_id'],
            months=dialog_manager.dialog_data['service_new_months'],
        )
    if dialog_manager.dialog_data.get('service_new_reminder'):
        await session.edit_date_subscription(
            service_id=dialog_manager.dialog_data['service_id'],
            reminder=datetime.fromisoformat(
                dialog_manager.dialog_data['service_new_reminder']
            ),
        )
    await session.commit()

    await callback.message.edit_text(l10n.format_value('Approve-sub-edit'))
    await dialog_manager.done()
    await dialog_manager.start(
        state=MainMenu.CONTROL, mode=StartMode.RESET_STACK
    )
