from datetime import datetime
from typing import Any

from aiogram_dialog import DialogManager


async def get_subs_for_delete(dialog_manager: DialogManager, **kwargs) -> dict[str, list[Any] | Any]:
    l10n = dialog_manager.middleware_data['l10n']
    session = dialog_manager.middleware_data['session']

    services = await session.get_services(
        user_id=dialog_manager.event.from_user.id
    )

    if not services:
        return {'message': l10n.format_value('nothing-output'), 'subs': []}

    subs = [
        (item.service_id, item.title, datetime.date(item.reminder).isoformat())
        for item in services
    ]
    return {'message': l10n.format_value('set-for-delete'), 'subs': subs}
