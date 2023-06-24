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
        Validator("redis.REDIS_HOST", must_exist=True),
        Validator("redis.REDIS_PORT", len_eq=4, cast=str, must_exist=True),
        Validator("redis.REDIS_DATABASE", gte=7, cast=int),

        Validator("postgres.POSTGRES_HOST", must_exist=True),
        Validator("postgres.POSTGRES_PORT", len_eq=4, cast=str, must_exist=True),
        Validator("postgres.POSTGRES_USERNAME", cast=str, must_exist=True),
        Validator("postgres.POSTGRES_PASSWORD", cast=str, must_exist=True),
        Validator("postgres.POSTGRES_DATABASE", cast=str, must_exist=True),
    ]
)

settings.validators.validate()
