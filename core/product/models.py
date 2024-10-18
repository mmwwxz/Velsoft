from django.core.exceptions import ValidationError
from django.db import models


class Color(models.Model):
    title = models.CharField(
        max_length=223,
        verbose_name='Название'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Цвет для товара'
        verbose_name_plural = 'Цвета для товаров'


class StorageLocation(models.Model):
    title = models.CharField(
        max_length=223,
        verbose_name='Название'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Место хранения товара'
        verbose_name_plural = 'Место хранения товаров'


class Product(models.Model):
    title = models.CharField(
        max_length=223,
        verbose_name='Название товара'
    )
    color = models.CharField(
        max_length=223,
        verbose_name='Цвет товара'
    )
    image = models.ImageField(
        upload_to='media/product_cover',
        verbose_name='Фото товара',
        blank=True,
        null=True,
        default='media/product_cover/default_photo.jpeg'
    )
    description = models.TextField(
        verbose_name='Описание товара',
        blank=True,
        null=True,
        help_text='Не обязательно'
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество товара'
    )
    purchase_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        verbose_name='Закупочная цена товара (в количестве 1-ой штуки)'
    )
    storage_location = models.ForeignKey(
        StorageLocation,
        on_delete=models.PROTECT,
        verbose_name='Место хранения товара'
    )
    sale_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        verbose_name='Цена продажи товара (в количестве 1-ой штуки)'
    )
    delivery_date = models.DateField(
        verbose_name='Дата завоза товара'
    )
    created_date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата создания объекта'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class SoldProduct(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name='Товар'
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество проданного товара'
    )
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Сумма продажи'
    )
    sale_date = models.DateField(
        verbose_name='Дата продажи товара'
    )
    description = models.TextField(
        verbose_name='Описание товара',
        blank=True,
        null=True,
        help_text='Не обязательно'
    )
    created_date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата создания объекта'
    )
    status = models.PositiveSmallIntegerField(
        choices=(
            (1, 'Выполнен'),
            (2, 'Отказано'),
            (3, 'В рассрочку'),
        ),
        default=1,
        verbose_name='Статус продажи'
    )

    # def clean(self):
    #     if self.total_price < 0.00:
    #         raise ValidationError({'total_price': 'Общая сумма продажи не может быть меньше 0'})
    #     return super(SoldProduct, self).clean()

    class Meta:
        verbose_name = 'Проданный товар'
        verbose_name_plural = 'Проданные товары'

    def __str__(self):
        return str(self.product)


