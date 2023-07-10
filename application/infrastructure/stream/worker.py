from contextlib import suppress

import nats
from aiogram import Bot
from ormsgpack.ormsgpack import unpackb

from application.core.misc.makers import maker


async def poll_nats(bot: Bot):
    nats_connect = await nats.connect(maker.nats_url.human_repr())
    js = nats_connect.jetstream()

    subscribe = await js.subscribe(
        subject="service_notify.message",
        durable="get_message"
    )

    while True:
        with suppress(TimeoutError):
            message = await subscribe.next_msg()
            await message.ack()

            data = unpackb(message.data)
            await bot.send_message(
                chat_id=data["user_id"],
                text=f'<b>🔔 Уведомление</b>\n<b>Напоминаем Вам</b>, что ваша подписка <b>{data["service"]}</b> '
                     f'скоро <b>закончится</b>!'
            )
