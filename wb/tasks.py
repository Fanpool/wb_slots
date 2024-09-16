from core.celery import app

from wb.services import update_wb_slots, update_wb_warehouses


@app.task(bind=True, ignore_result=True)
def repeat_update_slots(self):
    update_wb_slots()


@app.task(bind=True, ignore_result=True)
def repeat_update_warehouses(self):
    update_wb_warehouses()
