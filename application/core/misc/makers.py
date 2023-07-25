from yarl import URL

from application.core.config.config import settings


class URLMakers:
    # Variables for PostgreSQL
    database_host: str = settings['postgres.POSTGRES_HOST']
    database_port: int = settings['postgres.POSTGRES_PORT']
    database_username: str = settings['postgres.POSTGRES_USERNAME']
    database_password: str = settings['postgres.POSTGRES_PASSWORD']
    database_base: str = settings['postgres.POSTGRES_DATABASE']

    # Variables for Redis
    redis_host: str = settings['redis.REDIS_HOST']
    redis_port: int = settings['redis.REDIS_PORT']
    redis_base: int = settings['redis.REDIS_DATABASE']

    # Variables for NATS
    nats_host: str = settings['nats.NATS_HOST']
    nats_port: int = settings['nats.NATS_PORT']

    @property
    def database_url(self) -> URL:
        return URL.build(
            scheme='postgresql+asyncpg',
            host=self.database_host,
            port=self.database_port,
            user=self.database_username,
            password=self.database_password,
            path=f'/{self.database_base}'
        )

    @property
    def redis_url(self) -> URL:
        return URL.build(
            scheme='redis',
            host=self.redis_host,
            port=self.redis_port,
            path=f'/{self.redis_base}'
        )

    @property
    def nats_url(self) -> URL:
        return URL.build(
            scheme='nats',
            host=self.nats_host,
            port=self.nats_port
        )

