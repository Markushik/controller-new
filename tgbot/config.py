from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=[
        'configs//settings.toml',
        'configs//.secrets.toml'
    ],
    environments=True,
    env_switcher="ENV_FOR_DYNACONF",

)
