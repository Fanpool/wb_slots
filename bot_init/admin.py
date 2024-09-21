from django.contrib import admin
from django.conf import settings
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_object_actions import DjangoObjectActions, action

from bot_init.models import Message, Subscriber, AdminMessage


def tg_delete_messages(modeladmin, request, queryset):
    from bot_init.service import delete_messages
    """Функция для удаления сообщений из чата с ботом."""
    data = dict()
    for message in queryset:
        data.setdefault(message.chat_id, [])
        data[message.chat_id].append(message.message_id)
    for chat_id, message_id_list in data.items():
        delete_messages(chat_id, message_id_list)


tg_delete_messages.short_description = "Удалить сообщения в телеграмм"


@admin.register(Message)
class MessageAdmin(DjangoObjectActions, admin.ModelAdmin):
    """Конфигурация для админки."""

    list_display = ("display_chat_id", "display_direction", "text", "date")
    search_fields = ("text", "chat_id")
    actions = [tg_delete_messages]

    @admin.display(description='Чат')
    def display_chat_id(self, instance: Message):
        return mark_safe(f"""{instance.chat_id} (<a href="/admin/botinit/subscriber/{instance.chat_id}" target="_blank">Подписчик</a>)
        """)

    @admin.display(description='direction')
    def display_direction(self, instance: Message):
        if instance.from_user_id == settings.TG_BOT.id:
            return f'⬆'
        else:
            return f'⬇'

    display_direction.admin_order_field = 'from_user_id'


admin.site.register(Subscriber)
admin.site.register(AdminMessage)
