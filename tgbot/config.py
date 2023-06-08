from dynaconf import Dynaconf, Validator

settings = Dynaconf(  # TODO: add validation
    envvar_prefix="DYNACONF",
    settings_files=[
        'configs//settings.toml',
        'configs//.secrets.toml'
    ],
    environments=True
)

settings.validators.register(
    validators=[
        Validator("REDIS_HOST", must_exist=True, cast=str, env="default"),
        Validator("REDIS_PORT", must_exist=True, cast=int, env="default"),
        Validator("REDIS_DATABASE", must_exist=True, cast=int, env="default")
    ]
)

settings.validators.validate()
