from aiogram_dialog import DialogManager


async def get_service_data(
        dialog_manager: DialogManager,
        **kwargs
) -> None:
    return {
        'service_new': dialog_manager.dialog_data.get('service_new'),
        'service_old': dialog_manager.dialog_data.get('service_old'),
    }
