# Generated by Django 3.2.3 on 2021-07-03 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Homepage', '0013_order_remained_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='remaining_capacity',
            field=models.IntegerField(default=0),
        ),
    ]
