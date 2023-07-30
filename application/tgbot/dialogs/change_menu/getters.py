from aiogram_dialog import DialogManager


async def get_input_data(dialog_manager: DialogManager, **kwargs) -> None:
    return {'service': dialog_manager.dialog_data.get('service')}
