from core.settings.components import config


WB_TOKEN = config('WB_TOKEN')


WB_AUTH_HEADERS = {
    "Authorization": WB_TOKEN
}

COEFFICIENTS_URL = "https://supplies-api.wildberries.ru/api/v1/acceptance/coefficients"
WAREHOUSES_URL = "https://supplies-api.wildberries.ru/api/v1/warehouses"
