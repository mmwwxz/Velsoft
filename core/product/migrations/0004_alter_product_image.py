# Generated by Django 5.0.6 on 2024-06-18 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='media/media/product_cover/A7.jpeg', null=True, upload_to='media/product_cover', verbose_name='Фото товара'),
        ),
    ]