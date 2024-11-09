from django.core.management.base import BaseCommand

from backend.bot_init.service import update_webhook


class Command(BaseCommand):
    """Команда для обновления хоста с консоли."""

    help = 'command for update webhook'

    def handle(self, *args, **options):
        """Entrypoint."""
        update_webhook()
