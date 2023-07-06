import nats
from aiogram import Bot
from ormsgpack.ormsgpack import unpackb


async def poll_nats(bot: Bot):
    nc = await nats.connect('nats://127.0.0.1:4222')
    js = nc.jetstream()

    sub = await js.subscribe("service_notify.message")

    while True:
        try:
            msg = await sub.next_msg()
            await msg.ack()

            data = unpackb(msg.data)
            print(data)
            await bot.send_message(data[0], data[1])
        except TimeoutError:
            pass
