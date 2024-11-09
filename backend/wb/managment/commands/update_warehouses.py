from django.core.management import BaseCommand

from wb import services


class Command(BaseCommand):
    help = 'Search'

    def handle(self, *args, **kwargs):
        services.update_wb_warehouses()
