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
        Validator(
            names='API_TOKEN', condition=validate_token, must_exist=True
        ),
        Validator(
            names='redis.REDIS_HOST', is_type_of=int, must_exist=True
        ),
        Validator(
            names='redis.REDIS_PORT', is_type_of=int, must_exist=True
        ),
        Validator(
            names='redis.REDIS_DATABASE', is_type_of=int
        ),
        Validator(
            names='postgres.POSTGRES_HOST', is_type_of=str, must_exist=True
        ),
        Validator(
            names='postgres.POSTGRES_PORT', is_type_of=int, must_exist=True
        ),
        Validator(
            names='postgres.POSTGRES_USERNAME', is_type_of=str, must_exist=True
        ),
        Validator(
            names='postgres.POSTGRES_PASSWORD', is_type_of=str, must_exist=True
        ),
        Validator(
            names='postgres.POSTGRES_DATABASE', is_type_of=str, must_exist=True
        ),
        Validator(
            names='nats.NATS_HOST', is_type_of=str, must_exist=True
        ),
        Validator(
            names='nats.NATS_PORT', is_type_of=int, must_exist=True
        ),
    ]
)
settings.validators.validate()
