from aiogram.utils.token import validate_token
from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    settings_files=[
        'configs//settings.toml',
        'configs//.secrets.toml'
    ],
    environments=True,
)

settings.validators.register(
    validators=[
        Validator("API_TOKEN", condition=validate_token, must_exist=True),

        Validator("redis.REDIS_HOST", is_type_of=str, must_exist=True),
        Validator("redis.REDIS_PORT", is_type_of=int, cast=str, must_exist=True),
        Validator("redis.REDIS_DATABASE", is_type_of=int, cast=str),

        Validator("postgres.POSTGRES_HOST", is_type_of=str, must_exist=True),
        Validator("postgres.POSTGRES_PORT", is_type_of=int, must_exist=True),
        Validator("postgres.POSTGRES_USERNAME", is_type_of=str, must_exist=True),
        Validator("postgres.POSTGRES_PASSWORD", is_type_of=str, must_exist=True),
        Validator("postgres.POSTGRES_DATABASE", is_type_of=str, must_exist=True),

        Validator("nats.NATS_HOST", is_type_of=str, must_exist=True),
        Validator("nats.NATS_PORT", is_type_of=int, cast=str, must_exist=True),
    ]
)

settings.validators.validate()
