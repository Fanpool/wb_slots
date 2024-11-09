from rest_framework.viewsets import ModelViewSet

from backend.orders.models import Order
from backend.orders.serializers import OrderSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
