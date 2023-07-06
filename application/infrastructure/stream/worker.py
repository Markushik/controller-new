from contextlib import suppress

import nats
from aiogram import Bot
from ormsgpack.ormsgpack import unpackb

from application.core.config.config import settings


async def poll_nats(bot: Bot):
    nc = await nats.connect(f'nats://{settings["nats.NATS_HOST"]}:{settings["nats.NATS_PORT"]}')
    js = nc.jetstream()

    sub = await js.subscribe("service_notify.message")

    while True:
        with suppress(TimeoutError):
            msg = await sub.next_msg()
            await msg.ack()

            data = unpackb(msg.data)
            await bot.send_message(data[0], data[1])
