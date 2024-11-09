import datetime
from pytz import timezone

from backend.wb import models as wb_models
from backend.orders import models as order_models


def search_slot(order: order_models.Order):
    if not order.warehouses.exists():
        return wb_models.Slot.objects.none()

    slot_qs = (wb_models.Slot.objects
               .filter(box_type=order.box_type,
                       coefficient__lte=order.max_coefficient,
                       coefficient__gte=0,
                       warehouse__in=order.warehouses.all()))

    if slot_qs.exists():
        co, created = order_models.CompletedOrder.objects.get_or_create(order=order,
                                                                        slot=slot_qs.order_by('dt').first())
    return slot_qs


def search_slots():
    tz = timezone("Europe/Moscow")
    dt_now = datetime.datetime.now(tz=tz).date()
    order_qs = (order_models.Order.objects.filter(is_active=True)
                .select_related('box_type')
                .prefetch_related('warehouses'))
    slot_qs = (wb_models.Slot.objects
               .filter(dt__gt=dt_now)
               .select_related('warehouse', 'box_type'))

    res = {}

    for order in order_qs:
        for wh in order.warehouses.all():
            res[(wh.id, order.box_type_id)] = {'order': order, 'slots': []}

    for slot in slot_qs:
        key = (slot.warehouse_id, slot.box_type_id)
        if not res.get(key):
            continue
        d = res.get(key)
        if 0 <= slot.coefficient <= d['order'].max_coefficient:
            d['slots'].append(slot)

    for key, data in res.items():
        if len(data['slots']):
            sorted_slots = sorted(data['slots'], key=lambda x: x.dt)
            co, created = order_models.CompletedOrder.objects.get_or_create(order=data['order'],
                                                                            slot=sorted_slots[0])
    return res


def deactivate_outdated_orders():
    tz = timezone("Europe/Moscow")
    gdt = datetime.datetime.now(tz=tz) - datetime.timedelta(days=order_models.ORDER_LIFE_DAYS)
    for order in order_models.Order.objects.filter(is_active=True, created_at__lt=gdt):
        order.deactivate()
