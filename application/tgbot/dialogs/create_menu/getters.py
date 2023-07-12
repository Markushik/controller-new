from datetime import datetime

import asyncstdlib
from aiogram_dialog import DialogManager


async def get_subs_for_output(dialog_manager: DialogManager, **kwargs) -> None:
    l10n = dialog_manager.middleware_data["l10n"]
    session = dialog_manager.middleware_data["session"]

    services = await session.get_services(user_id=dialog_manager.event.from_user.id)
    print(services)
    subs = [f"<b>{count + 1}. {item.title}</b> — {datetime.date(item.reminder)}\n"
            async for count, item in asyncstdlib.enumerate(services)]
    print(subs)

    match subs:
        case []:
            return {"subs": l10n.format_value("Nothing-output")}
        case _:
            return {"subs": ''.join(subs)}


async def get_subs_for_delete(dialog_manager: DialogManager, **kwargs) -> None:
    l10n = dialog_manager.middleware_data["l10n"]
    session = dialog_manager.middleware_data["session"]

    services = await session.get_services(user_id=dialog_manager.event.from_user.id)
    subs = [(item.service_id, item.title, datetime.date(item.reminder).isoformat())
            for item in services]

    match subs:
        case []:
            return {"message": l10n.format_value("Nothing-output"), "subs": subs}
        case _:
            return {"message": l10n.format_value("Set-for-delete"), "subs": subs}
