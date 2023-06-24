"""
This file is responsible for displaying commands in the menu window
"""

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="▶️ Запустить бота"),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
