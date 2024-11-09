from core import celery_app

from wb.services import update_wb_slots, update_wb_warehouses


@celery_app.task(bind=True, ignore_result=True)
def repeat_update_slots(self):
    update_wb_slots()


@celery_app.task(bind=True, ignore_result=True)
def repeat_update_warehouses(self):
    update_wb_warehouses()
