from rest_framework.serializers import ModelSerializer

from backend.orders.models import Order


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
