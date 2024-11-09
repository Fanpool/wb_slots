from core.settings.components import config, BASE_DIR

DEBUG = False

ALLOWED_HOSTS = [
    config('DJANGO_DOMAIN_NAME'),
    'localhost',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('POSTGRES_HOST'),
        'PORT': config('POSTGRES_PORT', cast=int),
        'CONN_MAX_AGE': config('CONN_MAX_AGE', cast=int, default=60),
        'OPTIONS': {
            'connect_timeout': 10,
            'options': '-c statement_timeout=15000ms',
        },
    },
}

STATIC_PATH = config("STATIC_PATH")
STATIC_ROOT = STATIC_PATH if STATIC_PATH else BASE_DIR.parent / "static"

MEDIA_PATH = config("MEDIA_PATH")
MEDIA_ROOT = MEDIA_PATH if MEDIA_PATH else BASE_DIR.parent / "media"
