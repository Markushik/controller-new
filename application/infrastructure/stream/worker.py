import asyncio

import ormsgpack
import zstd
from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter, TelegramForbiddenError
from nats.js import JetStreamContext

from application.core.misc.logging import configure_logger
from application.tgbot.keyboards.inline import get_extension_menu

logger = configure_logger()


async def nats_polling(
        bot: Bot, i18n_middleware, jetstream: JetStreamContext
) -> None:
    subscribe = await jetstream.subscribe(
        subject='service_notify.message',
        stream='service_notify',
        durable='get_message',
        manual_ack=True,
    )

    async for message in subscribe.messages:
        try:
            data = ormsgpack.unpackb(zstd.decompress(message.data))

            chat_id = data['chat_id']
            language = data['language']
            service = data['service']
            months = data['months']

            l10n = i18n_middleware.l10ns[language]

            await bot.send_message(
                chat_id=chat_id,
                text=l10n.format_value(
                    'notification-message', {
                        'service': service
                    }
                ),
                reply_markup=get_extension_menu(
                    text=l10n.format_value('renew'),
                    service=service,
                    months=months,
                ),
            )
            await message.ack()

        except TimeoutError:
            pass
        except TelegramRetryAfter as ex:
            await logger.ainfo(f'Limit exceeded, continue in: {ex.retry_after}')
            await asyncio.sleep(float(ex.retry_after))
            continue
        except TelegramForbiddenError:
            await logger.ainfo('User blocked Bot')
            await message.ack()
            continue
        except BaseException as ex:
            await logger.aerror(f'Unexpected error: {ex}')
            continue
