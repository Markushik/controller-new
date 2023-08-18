from datetime import datetime

from aiogram_dialog import DialogManager


async def get_subs_for_edit(
        dialog_manager: DialogManager,
        **kwargs
) -> None:
    l10n = dialog_manager.middleware_data['l10n']
    session = dialog_manager.middleware_data['session']

    services = await session.get_services(
        user_id=dialog_manager.event.from_user.id
    )

    if not services:
        return {'message': l10n.format_value('Nothing-output'), 'subs': []}

    subs = [
        (item.service_id, item.title, datetime.date(item.reminder).isoformat())
        for item in services
    ]
    return {'message': l10n.format_value('Set-for-edit'), 'subs': subs}


async def get_service_title_data(
        dialog_manager: DialogManager,
        **kwargs
) -> None:
    return {
        'service_new_title': dialog_manager.dialog_data.get('service_new_title'),
        'service_old_title': dialog_manager.dialog_data.get('service_old_title'),
    }


async def get_service_months_data(
        dialog_manager: DialogManager,
        **kwargs
) -> None:
    return {
        'service_new_months': dialog_manager.dialog_data.get('service_new_months'),
        'service_old_months': dialog_manager.dialog_data.get('service_old_months'),
    }


async def get_service_reminder_data(
        dialog_manager: DialogManager,
        **kwargs
) -> None:
    return {
        'service_new_reminder': dialog_manager.dialog_data.get('service_new_reminder'),
        'service_old_reminder': dialog_manager.dialog_data.get('service_old_reminder'),
    }
