# Generated by Django 3.2.3 on 2021-06-20 22:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Homepage', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='line_item',
            name='id_line_item',
        ),
    ]