import telebot
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from loguru import logger

from bot_init.service import registration_subscriber
from bot_init.markup import InlineKeyboard
from bot_init.services.answer import Answer
from bot_init.utils import get_tbot_instance, save_message
from django.conf import settings

token = settings.TG_BOT.token
tbot = get_tbot_instance()

log = logger.bind(task="write_in_data")


@csrf_exempt
def bot(request):
    """Обработчик пакетов от телеграмма."""
    if request.content_type == 'application/json':
        json_data = request.body.decode('utf-8')
        log.info(json_data)
        update = telebot.types.Update.de_json(json_data)
        tbot.process_new_updates([update])
        return HttpResponse('')
    else:
        raise PermissionDenied


@tbot.message_handler(content_types=['text'])
def text(message):
    save_message(message)
    answer = Answer(f'Получено сообщение: {message.text}', message.chat.id, keyboard=[])
    answer.send()


@tbot.message_handler(commands=['help'])
def help(message):
    save_message(message)
    keyboard = InlineKeyboard((
        (("Mon", "0"),),
        (("Tue", "1"),),
        (("Wen", "2"),)
    ))
    answer = Answer('qwe', message.chat.id, keyboard=keyboard.keyboard)
    answer.send()


@tbot.message_handler(commands=['start'])
def start(message):
    save_message(message)
    registration_subscriber(message.chat.id)
    answer = Answer("Ведите фамилию!", message.chat.id)
    answer.send()
    tbot.register_next_step_handler(message, start_2)


def start_2(message):
    answer = Answer('Привет! {}\nответ неверный:'.format(message.text), message.chat.id)
    answer.send()
    answer = Answer('Рома чорт', message.chat.id)
    answer.send()

    tbot.send_invoice()
