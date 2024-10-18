import django_filters
from .models import Product, StorageLocation
from django import forms


class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title', lookup_expr='icontains', label='Название',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    color = django_filters.CharFilter(
        field_name='color', lookup_expr='icontains', label='Цвет',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description = django_filters.CharFilter(
        field_name='description', lookup_expr='icontains', label='Описание',
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    quantity = django_filters.NumberFilter(
        field_name='quantity', label='Количество',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    sale_price__gte = django_filters.NumberFilter(
        field_name='sale_price', lookup_expr='gte', label='Цена от',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    sale_price__lte = django_filters.NumberFilter(
        field_name='sale_price', lookup_expr='lte', label='Цена до',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    purchase_price = django_filters.NumberFilter(
        field_name='purchase_price', label='Цена закупки',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    storage_location = django_filters.ModelChoiceFilter(
        field_name='storage_location',
        queryset=StorageLocation.objects.all(),
        label='Место хранения',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    delivery_date__gt = django_filters.DateFilter(
        field_name='delivery_date', lookup_expr='gt', label='Дата доставки (от)',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    delivery_date__lt = django_filters.DateFilter(
        field_name='delivery_date', lookup_expr='lt', label='Дата доставки (до)',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Product
        fields = [
            'title',
            'color',
            'description',
            'quantity',
            'sale_price__gte',
            'sale_price__lte',
            'purchase_price',
            'storage_location',
            'delivery_date__gt',
            'delivery_date__lt'
        ]
