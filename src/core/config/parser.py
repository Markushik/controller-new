from dynaconf import Dynaconf

from .validator import validators

settings = Dynaconf(
    settings_files=[
        'configs//settings.toml',
        'configs//.secrets.toml'
    ],
    validators=validators,
    environments=True,
)
