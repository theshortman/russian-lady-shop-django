import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from catalog.models import Category, Product, ProductItem
from catalog.views import CategoryList


class CategoryListViewTest(APITestCase):
    def test_view_by_name(self):
        category = Category.objects.create(name='Test category name')

        resp = self.client.get(reverse('category-list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        categories = json.loads(resp.content)
        self.assertEqual(len(categories), 1)
        self.assertEqual(categories[0]['name'], category.name)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/api/v1/categories/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_pagination_is_disabled(self):
        self.assertIsNone(CategoryList().pagination_class)


class ProductListViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(
            name='Test category name', slug='test-category-slug')

        number_of_products = 23
        for product_num in range(1, number_of_products):
            product = Product.objects.create(
                category=category, name=f'Test product name {product_num}', slug=f'test-product-slug-{product_num}')
            ProductItem.objects.create(product=product, quantity=1)

    def test_view_url_exists_at_desired_location(self):
        category = Category.objects.get(id=1)

        resp = self.client.get(
            f'/api/v1/categories/{category.slug}/products/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_view_url_accessible_by_name(self):
        category = Category.objects.get(id=1)

        resp = self.client.get(reverse('product-list', args=[category.slug]))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_pagination_first_page(self):
        category = Category.objects.get(id=1)

        resp = self.client.get(reverse('product-list', args=[category.slug]))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        fetched_category = json.loads(resp.content)['category']
        products = fetched_category['products']
        self.assertEqual(len(products), 18)

        prev_page_number = fetched_category['prev_page_number']
        self.assertIsNone(prev_page_number)

        next_page_number = fetched_category['next_page_number']
        self.assertEqual(next_page_number, 2)

    def test_lists_second_page(self):
        category = Category.objects.get(id=1)

        resp = self.client.get(
            reverse('product-list', args=[category.slug])+'?page=2')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        fetched_category = json.loads(resp.content)['category']
        products = fetched_category['products']
        self.assertEqual(len(products), 4)

        prev_page_number = fetched_category['prev_page_number']
        self.assertEqual(prev_page_number, 1)

        next_page_number = fetched_category['next_page_number']
        self.assertIsNone(next_page_number)

    def test_view_category_does_not_exist(self):
        resp = self.client.get(
            '/api/v1/categories/category-not-exist-slug/products/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)


class ProductDetailViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(
            name='Test category name', slug='test-category-slug')
        Product.objects.create(
            category=category, name='Test product name', slug='test-product-slug')

    def test_view_by_name(self):
        category = Category.objects.get(id=1)
        product = Product.objects.get(id=1)

        resp = self.client.get(
            reverse('product-detail', args=[category.slug, product.slug]))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        product = json.loads(resp.content)
        self.assertEqual(product['name'], 'Test product name')

    def test_view_url_exists_at_desired_location(self):
        category = Category.objects.get(id=1)
        product = Product.objects.get(id=1)

        resp = self.client.get(
            f'/api/v1/categories/{category.slug}/products/{product.slug}/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_view_category_does_not_exist(self):
        resp = self.client.get(
            '/api/v1/categories/category-not-exist-slug/products/test-product-slug/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_view_product_does_not_exist(self):
        resp = self.client.get(
            '/api/v1/categories/test-category-slug/products/product-not-exist-slug/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
