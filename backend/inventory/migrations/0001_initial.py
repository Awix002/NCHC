# Generated by Django 5.0.2 on 2024-03-03 15:25

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='photos/%Y/%m/')),
                ('name', models.CharField(max_length=100)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('unit', models.CharField(max_length=100)),
                ('vendor', models.CharField(max_length=255)),
                ('purchase_date', models.DateField(default=datetime.date.today)),
                ('expiry_date', models.DateField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.category')),
            ],
        ),
    ]