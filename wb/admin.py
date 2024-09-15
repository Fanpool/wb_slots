from django.contrib import admin, messages
from django_object_actions import action, DjangoObjectActions

import wb.models as wb_models


@admin.register(wb_models.Warehouse)
class WarehouseAdmin(DjangoObjectActions, admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', 'address', 'work_time', 'accepts_qr')

    changelist_actions = ('action_update_warehouses',)

    @action(label='Обновить склады')
    def action_update_warehouses(self, request, queryset):
        from wb.services import update_wb_warehouses
        update_wb_warehouses()


@admin.register(wb_models.BoxType)
class BoxTypeAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name')


@admin.register(wb_models.Slot)
class SlotAdmin(DjangoObjectActions, admin.ModelAdmin):
    search_fields = ('warehouse__name', 'box_type__name')
    autocomplete_fields = ('warehouse', 'box_type')
    list_display = ('warehouse', 'box_type', 'dt', 'coefficient')
    fields = ('warehouse', 'box_type', 'dt', 'coefficient', 'unique_f')
    readonly_fields = ('unique_f',)

    changelist_actions = ('action_update_slots',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('warehouse', 'box_type')

    @action(label='Обновить слоты')
    def action_update_slots(self, request, queryset):
        from wb.services import update_wb_slots
        ret, mess = update_wb_slots()
        if ret == 0:
            messages.add_message(request, messages.SUCCESS, f'Успешно обновлено')
        else:
            messages.add_message(request, messages.ERROR, f'Ошибка при обновлении. {mess}')


@admin.register(wb_models.SlotUpdater)
class SlotUpdaterAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ('display_dt', 'error', 'error_text')

    changelist_actions = ('action_update_slots',)

    @admin.display(description='Дата')
    def display_dt(self, instance):
        return f'{instance.dt.strftime("%d.%m.%Y %H:%M:%S")}'
    display_dt.admin_order_field = 'dt'

    @action(label='Обновить слоты')
    def action_update_slots(self, request, queryset):
        from wb.services import update_wb_slots
        ret, mess = update_wb_slots()
        if ret == 0:
            messages.add_message(request, messages.SUCCESS, f'Успешно обновлено')
        else:
            messages.add_message(request, messages.ERROR, f'Ошибка при обновлении. {mess}')
