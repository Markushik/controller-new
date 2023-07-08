from contextlib import suppress

import nats
from aiogram import Bot
from ormsgpack.ormsgpack import unpackb

from application.core.misc.makers import maker


async def poll_nats(bot: Bot):
    nc = await nats.connect(str(maker.nats_url))
    js = nc.jetstream()

    sub = await js.subscribe("service_notify.message")

    while True:
        with suppress(TimeoutError):
            msg = await sub.next_msg()
            await msg.ack()

            data = unpackb(msg.data)
            await bot.send_message(data[0], data[1])
