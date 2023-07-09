from aiogram_dialog import DialogManager


async def get_langs_for_output(**kwargs) -> None:
    return {"langs": [item for item in enumerate([" 🇷🇺 Русский", " 🇬🇧 English"])]}


async def get_input_service_data(dialog_manager: DialogManager, **kwargs) -> None:
    return {
        "service": dialog_manager.dialog_data.get("service"),
        "months": dialog_manager.dialog_data.get("months"),
        "reminder": dialog_manager.dialog_data.get("reminder")
    }
