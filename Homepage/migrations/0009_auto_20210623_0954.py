# Generated by Django 3.2.3 on 2021-06-23 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Homepage', '0008_delete_reserve'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category_Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('description', models.TextField(blank=True, max_length=50, null=True)),
                ('crated_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('slug', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='food',
            name='category_food',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Homepage.category_food'),
        ),
    ]