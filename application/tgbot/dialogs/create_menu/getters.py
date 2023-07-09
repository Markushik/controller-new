from datetime import datetime

from aiogram_dialog import DialogManager


async def get_subs_for_output(dialog_manager: DialogManager, **kwargs) -> None:
    l10ns, lang = dialog_manager.middleware_data["l10ns"], dialog_manager.middleware_data["lang"]
    l10n = l10ns[lang]

    session = dialog_manager.middleware_data["session"]
    services = await session.get_services(user_id=dialog_manager.event.from_user.id)

    subs = [f"<b>{count + 1}. {item.Service.title}</b> — {datetime.date(item.Service.reminder)}\n"
            for count, item in enumerate(services)]

    match subs:
        case []:
            return {"subs": l10n.format_value("Nothing-output")}
        case _:
            return {"subs": ''.join(subs)}


async def get_subs_for_delete(dialog_manager: DialogManager, **kwargs) -> None:
    l10ns, lang = dialog_manager.middleware_data["l10ns"], dialog_manager.middleware_data["lang"]
    l10n = l10ns[lang]

    session = dialog_manager.middleware_data["session"]
    services = await session.get_services(user_id=dialog_manager.event.from_user.id)

    subs = [(item.Service.service_id, item.Service.title, datetime.date(item.Service.reminder).isoformat())
            for item in services]

    match subs:
        case []:
            return {"message": l10n.format_value("Nothing-output"), "subs": subs}
        case _:
            return {"message": l10n.format_value("Set-for-delete"), "subs": subs}
