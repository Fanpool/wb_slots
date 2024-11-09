from split_settings.tools import include, optional

from backend.core.settings.components import config

ENV = config('ENV') or 'development'

settings_pipeline = [
    "components/common.py",
    "components/celery.py",
    "components/mail.py",
    "components/logging.py",
    "components/rest_framework.py",
    "components/telegram.py",
    "components/wb.py",
    optional(f"environments/{ENV}.py"),
    optional("environments/local.py"),
]

include(*settings_pipeline)
