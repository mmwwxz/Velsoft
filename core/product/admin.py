from django.contrib import admin
from django.forms import DateInput
from django.db import models


from .models import Color, StorageLocation, Product, SoldProduct


class ProductAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.DateField: {'widget': DateInput(attrs={'type': 'date'})},
    }
    list_display = ('title', 'color', 'quantity', 'storage_location')


# admin.site.register(Color)
admin.site.register(StorageLocation)
admin.site.register(Product, ProductAdmin)
admin.site.register(SoldProduct)
