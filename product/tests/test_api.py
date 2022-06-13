from django.urls import reverse
from rest_framework import status

from rest_framework.test import APITestCase
from product.models import Product, Category, Brand, Color, SizeL
from product.serializers import ProductSerializer


class ProductApiTestCase(APITestCase):
    def setUp(self):
        self.show_size = SizeL.objects.create(name='testshow_size', slug='sizetest')
        self.color = Color.objects.create(color='testcolor', slug='colortest')
        self.category = Category.objects.create(title='test1', slug='test1')
        self.brand = Brand.objects.create(brand='firstbrand', slug='fortest1brand')

        self.product_1 = Product.objects.create(name='product1',
                                           category=self.category,
                                           description='for testing product1',
                                           selling_price=12,
                                           brand=self.brand,
                                           original_price=13,
                                           campaign = 'Test company2',
                                           color=self.color,
                                           show_size=self.show_size
                                           )
        self.product_2 = Product.objects.create(name='Test product2',
                                           category=self.category,
                                           description='for testing product2',
                                           selling_price=13,
                                           brand=self.brand,
                                           original_price=13,
                                           campaign='Test company2',
                                           color=self.color,
                                           show_size=self.show_size
                                           )

        self.product_3 = Product.objects.create(name='product3',
                                           category=self.category,
                                           description='for testing product3',
                                           selling_price=15,
                                           brand=self.brand,
                                           original_price=13,
                                           campaign = 'Test company2',
                                           color = self.color,
                                           show_size = self.show_size
                                           )

    def test_get(self):
        url = reverse('product-list')
        response = self.client.get(url)
        serializer_data = ProductSerializer([self.product_1, self.product_2, self.product_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse('product-list')
        response = self.client.get(url, data={'search': 'Test product2'})
        print(response.data)
        serializer_data = ProductSerializer([self.product_2, ], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter_price_from(self):
        url = reverse('product-list')
        response = self.client.get(url, data={'price_from': 13})
        serializer_data = ProductSerializer([self.product_2, self.product_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter_price_to(self):
        url = reverse('product-list')
        response = self.client.get(url, data={'price_to': 12})
        serializer_data = ProductSerializer([self.product_1, ], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)



