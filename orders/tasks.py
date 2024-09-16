from core.celery import app

from orders.services import search_slots


@app.task(bind=True)
def repeat_search_slots(self):
    search_slots()
