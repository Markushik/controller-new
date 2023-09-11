import asyncio
import logging

import lz4.frame
import ormsgpack
from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter, TelegramForbiddenError
from nats.js import JetStreamContext

from application.tgbot.keyboards.inline import get_extension_menu

logging.basicConfig(
    format='%(asctime)s | %(levelname)s | %(name)s:%(filename)s:%(lineno)d — %(message)s',
    encoding='utf-8',
    level='INFO',
)
logger = logging.getLogger(__name__)


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
            data = ormsgpack.unpackb(
                lz4.frame.decompress(message.data)
            )

            chat_id = data['chat_id']
            language = data['language']
            service = data['service']
            months = data['months']

            l10n = i18n_middleware.l10ns[language]

            await bot.send_message(
                chat_id=chat_id,
                text=l10n.format_value(
                    'Notification-message', {
                        'service': service
                    }
                ),
                reply_markup=get_extension_menu(
                    text=l10n.format_value('Renew-subscription'),
                    service=service,
                    months=months,
                ),
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
