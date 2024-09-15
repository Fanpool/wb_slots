import datetime

from django.db import models


class Warehouse(models.Model):
    name = models.CharField(
        max_length=200
    )
    address = models.CharField(
        max_length=250
    )
    work_time = models.CharField(
        max_length=100
    )
    accepts_qr = models.BooleanField(
        default=False
    )

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'
        ordering = []

    def __str__(self):
        return f'{self.name}'


class BoxType(models.Model):
    name = models.CharField(
        max_length=100
    )

    class Meta:
        verbose_name = 'Упаковка'
        verbose_name_plural = 'Упаковки'
        ordering = []

    def __str__(self):
        return f'{self.name}'


class Slot(models.Model):
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name='slots'
    )
    box_type = models.ForeignKey(
        BoxType,
        on_delete=models.CASCADE,
        related_name='slots'
    )
    coefficient = models.SmallIntegerField(
        default=-1
    )
    unique_f = models.CharField(
        max_length=100,
        unique=True,
        editable=False
    )
    dt = models.DateTimeField(
        default=datetime.datetime.now
    )

    class Meta:
        verbose_name = 'Слот'
        verbose_name_plural = 'Слоты'
        ordering = []

    def __str__(self):
        return f'[{self.dt.strftime("%d.%m.%Y %H:%M:%S")}] c={self.coefficient} {self.box_type_id}, {self.warehouse_id}'


class SlotUpdater(models.Model):
    dt = models.DateTimeField(
        auto_now_add=True
    )
    error = models.BooleanField(
        default=False
    )
    error_text = models.TextField(
        default=''
    )

    class Meta:
        verbose_name = 'Обновление'
        verbose_name_plural = 'Обновления'
        ordering = []

    def __str__(self):
        return f'{self.dt} {self.error}'
