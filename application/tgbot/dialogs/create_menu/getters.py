from datetime import datetime

from aiogram_dialog import DialogManager


async def get_subs_for_output(dialog_manager: DialogManager, **kwargs) -> dict[str, str]:
    l10n = dialog_manager.middleware_data['l10n']
    session = dialog_manager.middleware_data['session']

    services = await session.get_services(user_id=dialog_manager.event.from_user.id)

    if not services:
        return {'subs': l10n.format_value('nothing-output')}

    subs = [
        f'<b>{count}. {item.title}</b> — {datetime.date(item.reminder)}\n'
        for count, item in enumerate(iterable=services, start=1)
    ]
    return {'subs': ''.join(subs)}
