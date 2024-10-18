# Generated by Django 5.0.6 on 2024-06-16 14:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=223, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Цвет для товара',
                'verbose_name_plural': 'Цвета для товаров',
            },
        ),
        migrations.CreateModel(
            name='StorageLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=223, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Место хранения товара',
                'verbose_name_plural': 'Место хранения товаров',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=223, verbose_name='Название товара')),
                ('image', models.ImageField(upload_to='media/product_cover', verbose_name='Фото товара')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание товара')),
                ('quantity', models.PositiveSmallIntegerField(verbose_name='Количество товара')),
                ('purchase_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=12, verbose_name='Закупочная цена товара (в количестве 1-ой штуки)')),
                ('sale_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=12, verbose_name='Цена продажи товара (в количестве 1-ой штуки)')),
                ('delivery_date', models.DateField(verbose_name='Дата завоза товара')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Дата создания объекта')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.color', verbose_name='Цвет товара')),
                ('storage_location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.storagelocation', verbose_name='Место хранения товара')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
    ]
