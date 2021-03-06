# Generated by Django 3.2.3 on 2021-06-21 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Homepage', '0006_order_guest'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateTimeField(auto_now_add=True)),
                ('number_of_guest', models.IntegerField(default=1)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('hours_reserve', models.DateTimeField()),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Homepage.customer')),
                ('table', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Homepage.table')),
            ],
        ),
    ]
