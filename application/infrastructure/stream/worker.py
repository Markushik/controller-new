from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from nats.js import JetStreamContext
from ormsgpack.ormsgpack import unpackb


async def poll_nats(bot: Bot, i18n_middleware, jetstream: JetStreamContext) -> None:
    subscribe = await jetstream.subscribe(
        stream="service_notify",
        subject='service_notify.message',
        durable='get_message'
    )

    async for message in subscribe.messages:
        try:
            data = unpackb(message.data)

            user_id = data["user_id"]
            service = data["service_name"]
            language = data["language"]

            l10ns = i18n_middleware.l10ns
            l10n = l10ns[language]

            await bot.send_message(
                chat_id=user_id,
                text=l10n.format_value("Notification-message", {"service": service})
            )
            await message.ack()
        except TelegramForbiddenError:
            pass
        except TimeoutError:
            pass
