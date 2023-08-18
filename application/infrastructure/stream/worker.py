import asyncio

import lz4.frame
import ormsgpack
from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter
from loguru import logger
from nats.js import JetStreamContext

from application.tgbot.keyboards.inline import get_extension_menu


async def nats_polling(
        bot: Bot,
        i18n_middleware,
        jetstream: JetStreamContext
) -> None:
    subscribe = await jetstream.subscribe(
        stream='service_notify',
        subject='service_notify.message',
        durable='get_message',
        manual_ack=True,
    )

    async for message in subscribe.messages:
        try:
            data = ormsgpack.unpackb(
                lz4.frame.decompress(
                    message.data
                )
            )

            user_id = data['user_id']
            service = data['service']
            language = data['language']

            l10n = i18n_middleware.l10ns[language]

            await bot.send_message(
                chat_id=user_id,
                text=l10n.format_value(
                    'Notification-message', {
                        'service': service
                    }
                ),
                reply_markup=get_extension_menu(
                    l10n.format_value(
                        'Renew-subscription'
                    )
                )
            )
            await message.ack()

        except TimeoutError:
            pass
        except TelegramRetryAfter as ex:
            logger.info(f'Limit exceeded, continue in: {ex.retry_after}')
            await asyncio.sleep(float(ex.retry_after))
            continue
        except TelegramForbiddenError:
            logger.info('User blocked Bot')
            await message.ack()
            continue
        except BaseException as ex:
            logger.error(f'Unexpected error: {ex}')
            continue
