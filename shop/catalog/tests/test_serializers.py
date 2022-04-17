from django.test import TestCase, SimpleTestCase

from catalog.models import Category, Product, ProductItem, ProductImage
from catalog.serializers import CategorySerializer, ProductSerializer, ProductItemSerializer, ProductImageSerializer


class CategorySerializerTestCase(SimpleTestCase):
    def test_serializer_model(self):
        category_serializer = CategorySerializer()
        model = category_serializer.Meta.model
        self.assertEqual(model, Category)

    def test_serializer_fields(self):
        category_serializer = CategorySerializer()
        fields = category_serializer.Meta.fields
        self.assertEqual(fields, [
            'id',
            'name',
            'description',
            'slug'
        ])


class ProductItemSerializerTestCase(SimpleTestCase):
    def test_serializer_model(self):
        product_item_serializer = ProductItemSerializer()
        model = product_item_serializer.Meta.model
        self.assertEqual(model, ProductItem)

    def test_serializer_fields(self):
        product_item_serializer = ProductItemSerializer()
        fields = product_item_serializer.Meta.fields
        self.assertEqual(fields, [
            'id',
            'size',
            'quantity'
        ])


class ProductImageSerializerTestCase(SimpleTestCase):
    def test_serializer_model(self):
        product_image_serializer = ProductImageSerializer()
        model = product_image_serializer.Meta.model
        self.assertEqual(model, ProductImage)

    def test_serializer_fields(self):
        product_image_serializer = ProductImageSerializer()
        fields = product_image_serializer.Meta.fields
        self.assertEqual(fields, [
            'id',
            'image_large',
            'image_medium',
            'image_small'
        ])


class ProductSerializerTestCase(SimpleTestCase):
    def test_serializer_model(self):
        productSerializer = ProductSerializer()
        model = productSerializer.Meta.model
        self.assertEqual(model, Product)

    def test_serializer_fields(self):
        productSerializer = ProductSerializer()
        fields = productSerializer.Meta.fields
        self.assertEqual(fields, [
            'id',
            'name',
            'slug',
            'description',
            'detail',
            'price',
            'discount',
            'new_price',
            'product_images',
            'product_items'
        ])

    def test_serializer_product_items_field(self):
        product_serializer = ProductSerializer()
        product_items_field = product_serializer.get_fields()['product_items']
        self.assertIsInstance(product_items_field.child, ProductItemSerializer)
        self.assertEqual(product_items_field.many, True)
        self.assertEqual(product_items_field.read_only, True)

    def test_serializer_product_images_field(self):
        product_serializer = ProductSerializer()
        product_images_field = product_serializer.get_fields()['product_images']
        self.assertIsInstance(product_images_field.child, ProductImageSerializer)
        self.assertEqual(product_images_field.many, True)
        self.assertEqual(product_images_field.read_only, True)
