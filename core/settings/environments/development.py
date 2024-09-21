import logging
import socket

from core.settings.components import config, BASE_DIR

DEBUG = True

ALLOWED_HOSTS = [
    config('DJANGO_DOMAIN_NAME'),
    'localhost',
    '0.0.0.0',  # noqa: S104
    '127.0.0.1',
    '[::1]',
]

try:  # This might fail on some OS
    INTERNAL_IPS = [
        '{0}.1'.format(ip[:ip.rfind('.')])
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]
    ]
except socket.error:  # pragma: no cover
    INTERNAL_IPS = []
INTERNAL_IPS += ['127.0.0.1', '10.0.2.2']

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK':
        'server.settings.environments.development._custom_show_toolbar',
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',

    }
}
