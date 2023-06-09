import nats
from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from ormsgpack.ormsgpack import unpackb

from application.core.misc.makers import maker


async def poll_nats(bot: Bot):
    nats_connect = await nats.connect([maker.nats_url.human_repr(), ])
    js = nats_connect.jetstream()

    subscribe = await js.subscribe(
        stream="service_notify",
        subject='service_notify.message',
        durable='get_message'
    )

    while True:
        try:
            message = await subscribe.next_msg()
            await message.ack()

            data = unpackb(message.data)
            await bot.send_message(
                chat_id=data["user_id"],
                text=f'<b>🔔 Уведомление</b>\n'
                     f'<b>Напоминаем Вам</b>, что ваша подписка <code>{data["service_name"]}</code>'
                     f'скоро <b>закончится</b>!'
            )
        except TelegramForbiddenError:  # if user blocked bot
            pass
        except TimeoutError:
            pass
