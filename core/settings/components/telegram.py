from collections import namedtuple

import requests
from requests.exceptions import ConnectionError

from core.settings.components import config

TG_BOT = namedtuple('Bot', ['token', 'webhook_host', 'name', 'id'])
TG_BOT.token = config('TBOT_TOKEN')
TG_BOT.webhook_host = config('TBOT_HOST')

try:
    r = requests.get(f'https://api.telegram.org/bot{TG_BOT.token}/getMe').json()
    if not r.get('ok'):
        raise Exception('Data in .env is not valid')
    TG_BOT.name = r['result']['username']
    TG_BOT.id = r['result']['id']
except ConnectionError:
    raise Exception('Tbot not loaded')

TG_BOT.admins = list(map(int, config('TBOT_ADMINS').split(',')))
