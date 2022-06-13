from django_filters import rest_framework as filters

from .models import Product


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    filter_f = filters.CharFilter(field_name='category__filter_f', lookup_expr='icontains')
    price_from = filters.NumberFilter(field_name='selling_price', lookup_expr='gte')
    price_to = filters.NumberFilter(field_name='selling_price', lookup_expr='lte')
    # category = filters.CharFilter(field_name='category', lookup_expr='iexact')
    # brand = filters.CharFilter(field_name='brand', lookup_expr='iexact')
    class Meta:
        model = Product
        fields = ['name', 'price_from', 'price_to', 'category', 'brand', 'filter_f']


