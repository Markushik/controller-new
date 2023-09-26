from typing import Any

from aiogram_dialog import DialogManager

from src.presentation.tgbot.constants import LANGUAGES


async def get_langs_for_output(**kwargs) -> dict[str, list[Any]]:
    return {'langs': [item for item in enumerate(LANGUAGES)]}


async def get_input_service_data(
    dialog_manager: DialogManager, **kwargs
) -> dict[str, Any | None]:
    return {
        'service': dialog_manager.dialog_data.get('service'),
        'months': dialog_manager.dialog_data.get('months'),
        'reminder': dialog_manager.dialog_data.get('reminder'),
    }
