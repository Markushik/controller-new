from yarl import URL

from application.core.config.parser import settings


def create_postgres_url() -> URL:
    return URL.build(
        scheme='postgresql+asyncpg',
        host=settings['postgres.POSTGRES_HOST'],
        port=settings['postgres.POSTGRES_PORT'],
        user=settings['postgres.POSTGRES_USERNAME'],
        password=settings['postgres.POSTGRES_PASSWORD'],
        path=f"/{settings['postgres.POSTGRES_DATABASE']}",
    )


def create_redis_url() -> URL:
    return URL.build(
        scheme='redis',
        host=settings['redis.REDIS_HOST'],
        port=settings['redis.REDIS_PORT'],
        path=f"/{settings['redis.REDIS_DATABASE']}",
    )


def create_nats_url() -> URL:
    return URL.build(
        scheme='nats', host=settings['nats.NATS_HOST'], port=settings['nats.NATS_PORT']
    )
