# -*- coding: utf-8 -*-
"""
The main file responsible for launching the bot
"""

import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram_dialog import setup_dialogs
from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator, TranslatorHub
from loguru import logger
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.infrastructure.utils.logging import InterceptHandler
from handlers import client
from app.infrastructure.utils.config import settings
from app.tgbot.dialogs.create import dialog
from app.tgbot.dialogs.menu import main_menu
from app.tgbot.handlers import errors
from app.tgbot.middlewares.database import DbSessionMiddleware


# TODO: up with Docker
# TODO: edit ruff settings

async def main() -> None:
    """
    The main function responsible for launching the bot
    :return:
    """
    logging.basicConfig(
        handlers=[InterceptHandler()], level='DEBUG'
    )
    logger.add(
        '../../debug.log', format='{time} {level} {message}', level='DEBUG',
        colorize=True, encoding='utf-8', rotation='5 MB', compression='zip'
    )
    logger.info("LAUNCHING BOT")

    postgres_url = URL.create(
        drivername='postgresql+asyncpg', host=settings['postgres.POSTGRES_HOST'],
        port=settings['postgres.POSTGRES_PORT'], username=settings['postgres.POSTGRES_USERNAME'],
        password=settings['postgres.POSTGRES_PASSWORD'], database=settings['postgres.POSTGRES_DATABASE']
    )
    storage = RedisStorage.from_url(
        url=f"redis://{settings['redis.REDIS_HOST']}:{settings['redis.REDIS_PORT']}/{settings['redis.REDIS_DATABASE']}",
        key_builder=DefaultKeyBuilder(with_destiny=True)
    )

    translator_hub = TranslatorHub(
        {
            "ru": ("ru", "en"),
            "en": ("en",)
        },
        [
            FluentTranslator("ru", translator=FluentBundle.from_files('ru', filenames=['locales/ru.flt'])),
            FluentTranslator("en", translator=FluentBundle.from_files('en', filenames=['locales/en.flt']))
        ],
    )

    engine = create_async_engine(url=postgres_url, echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(token=settings['API_TOKEN'], parse_mode=ParseMode.HTML)
    disp = Dispatcher(storage=storage)

    disp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    # disp.update.middleware(ThrottlingMiddleware()) : TODO: ThrottlingMiddleware with NATS

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
        await bot.delete_webhook(drop_pending_updates=True)
        await disp.start_polling(bot, _translator_hub=translator_hub)
    finally:
        await disp.storage.close()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (SystemExit, KeyboardInterrupt, ConnectionRefusedError):
        logger.warning("SHUTDOWN BOT")
