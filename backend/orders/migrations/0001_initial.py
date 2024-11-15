# Generated by Django 5.1.1 on 2024-09-15 23:22

import datetime
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Заказчик',
                'verbose_name_plural': 'Заказчики',
                'ordering': [],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_coefficient', models.SmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(20), django.core.validators.MinValueValidator(0)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('notification_sent_date', models.DateTimeField(default=datetime.datetime.now)),
                ('box_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='wb.boxtype')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='orders.customer')),
                ('warehouses', models.ManyToManyField(blank=True, related_name='orders', to='wb.warehouse')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': [],
            },
        ),
        migrations.CreateModel(
            name='CompletedOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed_date', models.DateTimeField(auto_now_add=True)),
                ('slot', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comleted_orders', to='wb.slot')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='completed_orders', to='orders.order')),
            ],
            options={
                'verbose_name': 'Выполненный заказ',
                'verbose_name_plural': 'Выполненные Заказы',
                'ordering': [],
            },
        ),
    ]
