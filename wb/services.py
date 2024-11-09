import requests
import json
from django.conf import settings

from backend.wb import models as wb_models


def update_wb_slots():
    res = requests.get(settings.COEFFICIENTS_URL, headers=settings.AUTH_HEADERS)
    if res.status_code != 200:
        wb_models.SlotUpdater.objects.create(error=True, error_text=f'status_code = {res.status_code}.')
        return -1, f'status_code = {res.status_code}.'
    data = json.loads(res.text)
    box_type_dict = {}
    warehouse_dict = {}
    slot_objs = []
    for item in data:
        warehouse_dict[item["warehouseID"]] = item["warehouseName"]

        if item["boxTypeName"].strip() == "QR-поставка с коробами":
            item["boxTypeID"] = 100

        box_type_dict[item["boxTypeID"]] = item["boxTypeName"]

        tmp_slot = wb_models.Slot(
            warehouse_id=item["warehouseID"],
            box_type_id=item["boxTypeID"],
            coefficient=item["coefficient"],
            dt=item["date"]
        )
        tmp_slot.unique_f = f"{tmp_slot.warehouse_id}-{tmp_slot.box_type_id}-{tmp_slot.dt}"
        slot_objs.append(tmp_slot)

    box_type_objs = [wb_models.BoxType(id=k, name=v) for k, v in box_type_dict.items()]
    wb_models.BoxType.objects.bulk_create(box_type_objs,
                                          update_conflicts=True,
                                          update_fields=('name',),
                                          unique_fields=('id',),
                                          batch_size=1000)

    warehouse_objs = [wb_models.Warehouse(id=k, name=v) for k, v in warehouse_dict.items()]
    wb_models.Warehouse.objects.bulk_create(warehouse_objs,
                                            update_conflicts=True,
                                            update_fields=('name',),
                                            unique_fields=('id',),
                                            batch_size=1000)

    ret = wb_models.Slot.objects.bulk_create(slot_objs,
                                             update_conflicts=True,
                                             update_fields=('coefficient',),
                                             unique_fields=('unique_f',),
                                             batch_size=1000
                                             )
    wb_models.SlotUpdater.objects.create(error=False)
    return 0, ''


def update_wb_warehouses():
    res = requests.get(settings.WAREHOUSES_URL, headers=settings.AUTH_HEADERS)
    if res.status_code != 200:
        return None
    data = json.loads(res.text)
    wh_objs = []
    for item in data:
        wh_objs.append(wb_models.Warehouse(id=item["ID"],
                                           name=item["name"],
                                           address=item["address"],
                                           work_time=item["workTime"],
                                           accepts_qr=item["acceptsQR"]))
    wb_models.Warehouse.objects.bulk_create(wh_objs,
                                            update_conflicts=True,
                                            update_fields=('name', 'address', 'work_time', 'accepts_qr'),
                                            unique_fields=('id',))
