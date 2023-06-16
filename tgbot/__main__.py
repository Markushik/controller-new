# -*- coding: utf-8 -*-
"""
The main file responsible for launching the bot
"""

import asyncio

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram_dialog import setup_dialogs
from loguru import logger
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from handlers import client
from tgbot.config import settings
from tgbot.dialogs.create import dialog
from tgbot.dialogs.menu import main_menu
from tgbot.handlers import errors
# from tgbot.handlers.errors import dialogs_router
from tgbot.middlewares.database import DbSessionMiddleware


# class InterceptHandler(logging.Handler):
#     def emit(self, record):
#         try:
#             level = logger.level(record.levelname).name
#         except ValueError:
#             level = record.levelno
#
#         frame, depth = logging.currentframe(), 2
#         while frame.f_code.co_filename == logging.__file__:
#             frame = frame.f_back
#             depth += 1
#
#         logger.opt(depth=depth, exception=record.exc_info).log(
#             level, record.getMessage()
#         )


async def main() -> None:  # TODO: edit ruff settings
    """
    The main function responsible for launching the bot
    :return:
    """
    # logging.basicConfig(
    #     handlers=[InterceptHandler()], level=0
    # )
    logger.add(
        "../debug.log", format="{time} {level} {message}", level="DEBUG",
        colorize=True, encoding="utf-8", rotation="5 MB", compression="zip"
    )
    logger.info("LAUNCHING BOT")

    postgres_url = URL.create(
        drivername="postgresql+asyncpg", host=settings['postgres.POSTGRES_HOST'],
        port=settings['postgres.POSTGRES_PORT'], username=settings['postgres.POSTGRES_USERNAME'],
        password=settings['postgres.POSTGRES_PASSWORD'], database=settings['postgres.POSTGRES_DATABASE']
    )
    storage = RedisStorage.from_url(
        url=f"redis://{settings['redis.REDIS_HOST']}:{settings['redis.REDIS_PORT']}/{settings['redis.REDIS_DATABASE']}",
        key_builder=DefaultKeyBuilder(with_destiny=True)
    )

    bot = Bot(token=settings['API_TOKEN'], parse_mode=ParseMode.HTML)
    disp = Dispatcher(storage=storage)

    engine = create_async_engine(url=postgres_url, echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    disp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))  # TODO: all log update to loguru
    # disp.update.middleware(ThrottlingMiddleware())

    disp.callback_query.middleware(CallbackAnswerMiddleware())

    disp.include_routers(
        client.router,
        errors.router
    )
    disp.include_routers(
        dialog,
        main_menu
    )

    setup_dialogs(disp)

    try:
        await disp.start_polling(bot, allowed_updates=disp.resolve_used_update_types())
    finally:
        await disp.storage.close()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (SystemExit, KeyboardInterrupt, ConnectionRefusedError):
        logger.warning("SHUTDOWN BOT")
