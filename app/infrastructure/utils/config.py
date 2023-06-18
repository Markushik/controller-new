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
        Validator("redis.REDIS_HOST", must_exist=True),  # TODO: add validation
        Validator("redis.REDIS_PORT", must_exist=True),
        Validator("redis.REDIS_DATABASE", must_exist=True),

        Validator("postgres.POSTGRES_HOST", must_exist=True),
        Validator("postgres.POSTGRES_PORT", must_exist=True),
        Validator("postgres.POSTGRES_USERNAME", must_exist=True),
        Validator("postgres.POSTGRES_PASSWORD", must_exist=True),
        Validator("postgres.POSTGRES_DATABASE", must_exist=True),
    ]
)

settings.validators.validate()
