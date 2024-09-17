from django.core.management.base import BaseCommand
from loguru import logger
from django.conf import settings


log = logger.bind(task="app")


class Command(BaseCommand):
    """Команда для запуска бота в режиме long polling."""

    help = 'command for start bot long polling mode'

    def handle(self, *args, **options):
        """Entrypoint."""
        import telebot

        print(settings.TG_BOT.token)
        bot = telebot.TeleBot(settings.TG_BOT.token)

        @bot.message_handler(commands=['start'])
        def start_message(message):
            bot.send_message(message.chat.id, 'Привет')

        bot.polling()
