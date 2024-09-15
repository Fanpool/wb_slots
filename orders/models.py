import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


ORDER_LIFE_DAYS = 14


class Customer(models.Model):
    username = models.CharField(
        max_length=50,
        unique=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'
        ordering = []

    def __str__(self):
        return f'{self.username}'


class Order(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    warehouses = models.ManyToManyField(
        'wb.Warehouse',
        related_name='orders',
        blank=True
    )
    box_type = models.ForeignKey(
        'wb.BoxType',
        on_delete=models.CASCADE,
        related_name='orders'
    )
    max_coefficient = models.SmallIntegerField(
        default=0,
        validators=[
            MaxValueValidator(20),
            MinValueValidator(0)
        ]
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    is_active = models.BooleanField(
        default=True
    )
    notification_sent_date = models.DateTimeField(
        default=datetime.datetime.now
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = []

    def __str__(self):
        return f'{self.customer_id} {self.box_type_id} c={self.max_coefficient}'

    def deactivate(self):
        self.is_active = False
        self.save()


class CompletedOrder(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
        related_name='completed_orders'
    )
    slot = models.ForeignKey(
        'wb.Slot',
        on_delete=models.SET_NULL,
        null=True,
        related_name='comleted_orders'
    )
    completed_date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Выполненный заказ'
        verbose_name_plural = 'Выполненные Заказы'
        ordering = []

    def __str__(self):
        return f'{self.order_id}'
