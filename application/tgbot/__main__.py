# -*- coding: utf-8 -*-
"""
The main file responsible for launching the bot
"""

import asyncio
import logging

import nats
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState
from loguru import logger
from nats.aio.client import Client
from nats.js import JetStreamContext
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)

from application.core.config.config import settings
from application.core.misc.logging import InterceptHandler
from application.core.misc.makers import maker
from application.infrastructure.stream.worker import nats_polling
from application.tgbot.dialogs.change_menu.dialog import change_menu
from application.tgbot.dialogs.create_menu.dialog import create_menu
from application.tgbot.dialogs.delete_menu.dialog import delete_menu
from application.tgbot.dialogs.main_menu.dialog import main_menu
from application.tgbot.handlers import client
from application.tgbot.handlers.errors import on_unknown_intent, on_unknown_state
from application.tgbot.middlewares.database import DbSessionMiddleware
from application.tgbot.middlewares.i18n import make_i18n_middleware, I18nMiddleware


async def _main() -> None:
    """
    The main function responsible for launching the bot
    :return:
    """

    logging.basicConfig(handlers=[InterceptHandler()], level='INFO')
    logger.add(
        '../../debug.log', format='{time} {level} {message}', level='INFO',
        enqueue=True, colorize=True, encoding='utf-8', rotation='10 MB', compression='zip'
    )

    storage: RedisStorage = RedisStorage.from_url(
        url=maker.create_redis_url.human_repr(),
        key_builder=DefaultKeyBuilder(with_destiny=True, with_bot_id=True)
    )

    nats_connect: Client = await nats.connect(
        servers=[maker.create_nats_url.human_repr(), ]
    )
    jetstream: JetStreamContext = nats_connect.jetstream()

    async_engine: AsyncEngine = create_async_engine(
        url=maker.create_postgres_url.human_repr(),
        pool_pre_ping=True,
        echo=False
    )
    async_session: AsyncSession = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=True
    )

    bot: Bot = Bot(token=settings['API_TOKEN'], parse_mode=ParseMode.HTML)
    disp: Dispatcher = Dispatcher(storage=storage, events_isolation=storage.create_isolation())

    i18n_middleware: I18nMiddleware = make_i18n_middleware()

    disp.message.middleware(i18n_middleware)
    disp.callback_query.middleware(i18n_middleware)

    disp.update.outer_middleware(DbSessionMiddleware(session_maker=async_session))

    disp.include_router(client.router)
    disp.include_routers(
        main_menu,
        create_menu,
        change_menu,
        delete_menu
    )

    disp.errors.register(on_unknown_intent, ExceptionTypeFilter(UnknownIntent))
    disp.errors.register(on_unknown_state, ExceptionTypeFilter(UnknownState))

    setup_dialogs(disp)

    logger.info("LAUNCHING BOT")

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await asyncio.gather(
            nats_polling(bot, i18n_middleware, jetstream),
            disp.start_polling(bot)
        )
    finally:
        await storage.close()
        await bot.session.close()
        await async_engine.dispose()
        await nats_connect.drain()
        await logger.complete()


if __name__ == "__main__":
    try:
        # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) # for psycopg
        asyncio.run(_main())
    except (SystemExit, KeyboardInterrupt):
        logger.warning("SHUTDOWN BOT")
