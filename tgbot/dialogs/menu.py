"""
🗂 Мои подписки
🆘 Поддержка 💰 Донаты

"""
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Jinja

from tgbot.states.user import UserSG

main_menu = Dialog(
    Window(
        Jinja("help"),
        state=UserSG.help,
    )
)
