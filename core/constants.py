import enum
from core.settings import AppSettings


settings = AppSettings()

class Language(str, enum.Enum):
    KOREA = "KO"
    ENGLISH = "EN"
    JAPAN = "JA"


TORTOISE_ORM = {
    'connections': {
        'default': settings.database_url
    },
    'apps': {
        'models': {
            'models': [
                'aerich.models',
                'models'
            ],
            'default_connection': 'default',
        },
    },
}

# aerich: aerich init -t core.constants.TORTOISE_ORM
# shell: tortoise-cli -c core.constants.TORTOISE_ORM shell
