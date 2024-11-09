import os
from core.settings.components import BASE_DIR


LOG_DIR = BASE_DIR.parent / "logs"
LOG_DEBUG_PATH = LOG_DIR / "debug.log"
LOG_INFO_PATH = LOG_DIR / "info.log"

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {"format": "[%(name)-12s] %(levelname)-8s %(message)s"},
        "file": {"format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "console"},
        "file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "formatter": "file",
            "filename": LOG_DEBUG_PATH,
        },
        "file_info": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "formatter": "file",
            "filename": LOG_INFO_PATH,
        },
    },
    "loggers": {
        "": {"level": "WARNING", "handlers": ["console", "file", "file_info"]},
        "django.request": {
            "handlers": ["file"],
            "propagate": False,
            "level": "WARNING",
        },
    },
}