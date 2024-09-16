from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from django_object_actions import action, DjangoObjectActions

from . import models


@admin.register(models.Customer)
class CustomerAdmin(DjangoObjectActions, admin.ModelAdmin):
    search_fields = ('username',)
    list_display = ('username',)


class WarehouseInline(admin.StackedInline):
    autocomplete_fields = ('warehouse',)
    model = models.Order.warehouses.through
    can_add = False
    extra = 0


@admin.register(models.Order)
class OrderAdmin(DjangoObjectActions, admin.ModelAdmin):
    search_fields = ('customer__username', 'warehouses__name', 'box_type__name')
    autocomplete_fields = ('customer', 'box_type')

    list_display = ('customer', 'box_type', 'max_coefficient')
    list_select_related = ('customer', 'box_type')

    fields = ('customer', 'box_type', 'max_coefficient')

    inlines = (WarehouseInline,)

    change_actions = ('action_search_slot',)
    changelist_actions = ('action_search_slots',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('warehouses', )

    @action(label='Поиск слотов')
    def action_search_slots(self, request, queryset):
        from .services import search_slots
        res = search_slots()
        customers = []
        for k, v in res.items():
            if v['slots']:
                customers.append(v['order'].customer)
        mess = '<br>'.join([f'{customer.username}' for customer in customers])
        messages.add_message(request, messages.SUCCESS, mark_safe(f'Поиск завершен. Найдено для:<br> {mess}'))

    @action(label='Поиск слота')
    def action_search_slot(self, request, obj: models.Order):
        from .services import search_slot
        qs = search_slot(obj)
        if qs:
            mess = '<br>'.join([f'{slot.warehouse.name} {slot.dt}' for slot in qs[:10]])
            mess = f'{mess}<br>...'
            messages.add_message(request, messages.SUCCESS, mark_safe(f'Найдено {qs.count()}.<br> {mess}'))
            return
        messages.add_message(request, messages.WARNING, f'Слотов не найдено. Склады не должны быть пустыми')


@admin.register(models.CompletedOrder)
class CompletedOrderAdmin(admin.ModelAdmin):
    search_fields = ('order__customer__username', 'order__warehouses__name', 'order__box_type__name')
    autocomplete_fields = ('order',)
    list_display = ('order__customer', 'display_dt', 'order__box_type', 'order__max_coefficient', 'display_slot_dt', 'slot__warehouse', 'display_slot_K')
    list_select_related = ('order', 'order__customer', 'order__box_type', 'slot', 'slot__warehouse')

    @admin.display(description='Дата нахождения')
    def display_dt(self, instance):
        return f'{instance.completed_date.strftime("%d.%m.%Y %H:%M:%S")}'
    display_dt.admin_order_field = 'completed_date'

    @admin.display(description='Дата слота')
    def display_slot_dt(self, instance):
        return f'{instance.slot.dt.strftime("%d.%m.%Y %H:%M:%S")}'
    display_dt.admin_order_field = 'slot__dt'

    @admin.display(description='Max K')
    def display_max_K(self, instance: models.CompletedOrder):
        return f'{instance.order.max_coefficient}'
    display_max_K.admin_order_field = 'order__max_coefficient'

    @admin.display(description='Текущий K')
    def display_slot_K(self, instance: models.CompletedOrder):
        return f'{instance.slot.coefficient}'
    display_slot_K.admin_order_field = 'slot__coefficient'
