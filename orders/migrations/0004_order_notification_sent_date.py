# Generated by Django 5.1.1 on 2024-09-15 19:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_completedorder_slot'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='notification_sent_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
