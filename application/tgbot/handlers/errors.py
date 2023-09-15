from aiogram_dialog import DialogManager, StartMode

from application.core.misc.logging import configure_logger
from application.tgbot.states.user import MainMenu

logger = configure_logger()


async def on_unknown_intent(event, dialog_manager: DialogManager):
    await logger.aerror('Restarting dialog: %s', event.exception)
    await dialog_manager.start(state=MainMenu.MAIN, mode=StartMode.RESET_STACK)


async def on_unknown_state(event, dialog_manager: DialogManager):
    await logger.aerror('Restarting dialog: %s', event.exception)
    await dialog_manager.start(state=MainMenu.MAIN, mode=StartMode.RESET_STACK)
