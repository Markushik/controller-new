import asyncio

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from nats.js import JetStreamContext
from ormsgpack.ormsgpack import unpackb


async def poll_nats(
        bot: Bot,
        i18n_middleware,
        jetstream: JetStreamContext
) -> None:
    subscribe = await jetstream.subscribe(
        stream="service_notify",
        subject='service_notify.message',
        durable='get_message'
    )

    while True:
        try:
            message = await subscribe.next_msg()
            await message.ack()

            data = unpackb(message.data)

            l10ns = i18n_middleware.l10ns
            l10n = l10ns[data["language"]]

            await bot.send_message(
                chat_id=data["user_id"],
                text=l10n.format_value(
                    "Notification-message", {"service": data["service_name"]}
                )
            )
        except TelegramForbiddenError:  # if user blocked bot
            pass
        except asyncio.TimeoutError:
            pass
