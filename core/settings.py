import os
import pytz
import dotenv
from pathlib import Path
from django.utils import timezone
from loguru import logger

dotenv.load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

if os.getenv('DJANGO_SETTINGS') == 'production':
    DEBUG = False
else:
    DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_object_actions',
    'django_celery_beat',
    'wb',
    'orders',
    'bot_init',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

timezone.activate(pytz.timezone(TIME_ZONE))
timezone.localtime(timezone.now())

STATIC_URL = 'static/'
STATIC_PATH = os.environ.get("STATIC_PATH")
STATIC_ROOT = STATIC_PATH if STATIC_PATH else BASE_DIR / "static"

MEDIA_URL = 'media/'
MEDIA_PATH = os.environ.get("MEDIA_PATH")
MEDIA_ROOT = MEDIA_PATH if MEDIA_PATH else BASE_DIR / "media"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOG_DIR = BASE_DIR / "logs"
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

logger.add(f"{BASE_DIR}/logs/in_data.log", filter=lambda record: record["extra"]["task"] == "write_in_data")
logger.add(f"{BASE_DIR}/logs/out_data.log", filter=lambda record: record["extra"]["task"] == "write_out_data")
logger.add(f"{BASE_DIR}/logs/app.log", filter=lambda record: record["extra"]["task"] == "app")

COEFFICIENTS_URL = "https://supplies-api.wildberries.ru/api/v1/acceptance/coefficients"
WAREHOUSES_URL = "https://supplies-api.wildberries.ru/api/v1/warehouses"

TOKEN = os.getenv("TOKEN")

AUTH_HEADERS = {
    "Authorization": TOKEN
}

REDIS_HOST = "0.0.0.0"
REDIS_PORT = "6379"

CELERY_BROKER_URL = "redis://" + REDIS_HOST + ":" + REDIS_PORT + "/0"
CELERY_BROKER_TRANSPORT_OPTIONS = {"visibility_timeout": 3600}
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_RESULT_BACKEND = "redis://" + REDIS_HOST + ":" + REDIS_PORT + "/0"

CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

from collections import namedtuple

import requests
from requests.exceptions import ConnectionError

TG_BOT = namedtuple('Bot', ['token', 'webhook_host', 'name', 'id'])
TG_BOT.token = os.getenv('BOT_TOKEN')
TG_BOT.webhook_host = os.getenv('HOST')

try:
    r = requests.get(f'https://api.telegram.org/bot{TG_BOT.token}/getMe').json()
    if not r.get('ok'):
        raise Exception('Data in .env is not valid')
    TG_BOT.name = r['result']['username']
    TG_BOT.id = r['result']['id']
except ConnectionError:
    pass

TG_BOT.admins = list(map(int, os.getenv('ADMINS').split(',')))
