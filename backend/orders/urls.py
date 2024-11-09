from django.urls import path, include

from rest_framework.routers import SimpleRouter

from orders.views import WebAppView
from orders.viewsets import OrderViewSet


router = SimpleRouter()
router.register('orders', OrderViewSet)


app_name = 'orders'
urlpatterns = [
    path('webapp', WebAppView.as_view(), name='webapp'),
    path('', include(router.urls)),
]
