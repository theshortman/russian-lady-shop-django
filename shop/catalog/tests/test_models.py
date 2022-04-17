import os
import shutil
import uuid
from PIL import Image

from django.test import TestCase
from django.db import models
from django.core.files import File
from django.core.validators import MaxValueValidator, MinValueValidator

from shop.settings import MEDIA_ROOT
from catalog.models import Category, Product, ProductImage, ProductItem


class CategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Test name', slug='test-slug')

    def test_name_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)

    def test_name_unique(self):
        category = Category.objects.get(id=1)
        unique = category._meta.get_field('name').unique
        self.assertEqual(unique, True)

    def test_description_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_slug_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('slug').verbose_name
        self.assertEqual(field_label, 'slug')

    def test_slug_unique(self):
        category = Category.objects.get(id=1)
        unique = category._meta.get_field('slug').unique
        self.assertEqual(unique, True)

    def test_slug_db_index(self):
        category = Category.objects.get(id=1)
        db_index = category._meta.get_field('slug').db_index
        self.assertEqual(db_index, True)

    def test_sort_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('sort').verbose_name
        self.assertEqual(field_label, 'sort')

    def test_sort_default(self):
        category = Category.objects.get(id=1)
        default = category._meta.get_field('sort').default
        self.assertEqual(default, 0)

    def test_ordering(self):
        category = Category.objects.get(id=1)
        ordering = category._meta.ordering
        self.assertEqual(ordering, ['sort'])

    def test_object_name_is_name(self):
        category = Category.objects.get(id=1)
        expected_object_name = category.name
        self.assertEqual(str(category), expected_object_name)


class ProductModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(
            name='Test category name')
        Product.objects.create(
            category=category, name='Test product name')

    def test_category_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('category').verbose_name
        self.assertEqual(field_label, 'category')

    def test_category_field_related_model(self):
        product = Product.objects.get(id=1)
        related_model = product._meta.get_field('category').related_model
        self.assertEqual(related_model, Category)

    def test_category_field_related_name(self):
        product = Product.objects.get(id=1)
        related_name = product._meta.get_field(
            'category').remote_field.related_name
        self.assertEqual(related_name, 'products')

    def test_category_field_on_detele(self):
        product = Product.objects.get(id=1)
        on_detele = product._meta.get_field(
            'category').remote_field.on_delete
        self.assertEqual(on_detele, models.CASCADE)

    def test_name_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)

    def test_name_unique(self):
        product = Product.objects.get(id=1)
        unique = product._meta.get_field('name').unique
        self.assertEqual(unique, True)

    def test_description_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_detail_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('detail').verbose_name
        self.assertEqual(field_label, 'detail')

    def test_slug_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('slug').verbose_name
        self.assertEqual(field_label, 'slug')

    def test_slug_unique(self):
        product = Product.objects.get(id=1)
        unique = product._meta.get_field('slug').unique
        self.assertEqual(unique, True)

    def test_slug_db_index(self):
        product = Product.objects.get(id=1)
        db_index = product._meta.get_field('slug').db_index
        self.assertEqual(db_index, True)

    def test_price_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('price').verbose_name
        self.assertEqual(field_label, 'price')

    def test_price_default(self):
        product = Product.objects.get(id=1)
        default = product._meta.get_field('price').default
        self.assertEqual(default, 0)

    def test_discount_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('discount').verbose_name
        self.assertEqual(field_label, 'discount')

    def test_discount_default(self):
        product = Product.objects.get(id=1)
        default = product._meta.get_field('discount').default
        self.assertEqual(default, 0)

    def test_discount_validators(self):
        product = Product.objects.get(id=1)
        validators = product._meta.get_field('discount').validators
        self.assertEqual(
            validators, [MinValueValidator(0), MaxValueValidator(100)])

    def test_date_added_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('date_added').verbose_name
        self.assertEqual(field_label, 'date added')

    def test_date_added_auto_now_add(self):
        product = Product.objects.get(id=1)
        auto_now_add = product._meta.get_field('date_added').auto_now_add
        self.assertEqual(auto_now_add, True)

    def test_new_price_is_equals_price_if_discount_is_less_then_1(self):
        product = Product.objects.get(id=1)
        self.assertEqual(product.new_price, product.price)

    def test_new_price_is_less_price_if_discount_is_greater_then_0(self):
        product = Product(discount=50, price=1000)
        self.assertEqual(product.new_price, 500)

    def test_ordering(self):
        product = Product.objects.get(id=1)
        ordering = product._meta.ordering
        self.assertEqual(ordering, ['-date_added'])

    def test_object_name_is_name(self):
        product = Product.objects.get(id=1)
        expected_object_name = product.name
        self.assertEqual(str(product), expected_object_name)


class ProductImageModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(
            name='Test category name')
        product = Product.objects.create(
            category=category, name='Test product name')

        ProductImage.objects.create(product=product)

    def test_product_label(self):
        product_image = ProductImage.objects.get(id=1)
        field_label = product_image._meta.get_field('product').verbose_name
        self.assertEqual(field_label, 'product')

    def test_product_field_related_model(self):
        product_image = ProductImage.objects.get(id=1)
        related_model = product_image._meta.get_field('product').related_model
        self.assertEqual(related_model, Product)

    def test_product_field_related_name(self):
        product_image = ProductImage.objects.get(id=1)
        related_name = product_image._meta.get_field(
            'product').remote_field.related_name
        self.assertEqual(related_name, 'product_images')

    def test_product_field_on_detele(self):
        product_image = ProductImage.objects.get(id=1)
        on_detele = product_image._meta.get_field(
            'product').remote_field.on_delete
        self.assertEqual(on_detele, models.CASCADE)

    def test_image_large_label(self):
        product_image = ProductImage.objects.get(id=1)
        field_label = product_image._meta.get_field('image_large').verbose_name
        self.assertEqual(field_label, 'Large image')

    def test_image_large_upload_to(self):
        product_image = ProductImage.objects.get(id=1)
        upload_to = product_image._meta.get_field('image_large').upload_to
        self.assertEqual(upload_to, ProductImage.get_file_path)

    def test_image_large_blank(self):
        product_image = ProductImage.objects.get(id=1)
        blank = product_image._meta.get_field('image_large').blank
        self.assertEqual(blank, True)

    def test_image_large_max_length(self):
        product_image = ProductImage.objects.get(id=1)
        max_length = product_image._meta.get_field('image_large').max_length
        self.assertEqual(max_length, 255)

    def test_image_medium_label(self):
        product_image = ProductImage.objects.get(id=1)
        field_label = product_image._meta.get_field(
            'image_medium').verbose_name
        self.assertEqual(field_label, 'Medium image')

    def test_image_medium_upload_to(self):
        product_image = ProductImage.objects.get(id=1)
        upload_to = product_image._meta.get_field('image_medium').upload_to
        self.assertEqual(upload_to, ProductImage.get_file_path)

    def test_image_medium_blank(self):
        product_image = ProductImage.objects.get(id=1)
        blank = product_image._meta.get_field('image_medium').blank
        self.assertEqual(blank, True)

    def test_image_medium_max_length(self):
        product_image = ProductImage.objects.get(id=1)
        max_length = product_image._meta.get_field('image_medium').max_length
        self.assertEqual(max_length, 255)

    def test_image_small_label(self):
        product_image = ProductImage.objects.get(id=1)
        field_label = product_image._meta.get_field('image_small').verbose_name
        self.assertEqual(field_label, 'Small image')

    def test_image_small_upload_to(self):
        product_image = ProductImage.objects.get(id=1)
        upload_to = product_image._meta.get_field('image_small').upload_to
        self.assertEqual(upload_to, ProductImage.get_file_path)

    def test_image_small_blank(self):
        product_image = ProductImage.objects.get(id=1)
        blank = product_image._meta.get_field('image_small').blank
        self.assertEqual(blank, True)

    def test_image_small_max_length(self):
        product_image = ProductImage.objects.get(id=1)
        max_length = product_image._meta.get_field('image_small').max_length
        self.assertEqual(max_length, 255)

    def test_sort_label(self):
        product_image = ProductImage.objects.get(id=1)
        field_label = product_image._meta.get_field('sort').verbose_name
        self.assertEqual(field_label, 'sort')

    def test_sort_default(self):
        product_image = ProductImage.objects.get(id=1)
        default = product_image._meta.get_field('sort').default
        self.assertEqual(default, 0)

    def test_ordering(self):
        product_image = ProductImage.objects.get(id=1)
        ordering = product_image._meta.ordering
        self.assertEqual(ordering, ['product__name', 'sort'])

    def test_object_name_is_product_name(self):
        product_image = ProductImage.objects.get(id=1)
        expected_object_name = product_image.product.name
        self.assertEqual(str(product_image), expected_object_name, )

    def test_get_file_path(self):
        product_image = ProductImage()
        path = product_image.get_file_path('image.jpg')

        head, tail = os.path.split(path)
        self.assertEqual(head, 'product_images')

        filename, extension = tail.split('.')

        # If the filename is not valid uuid, exception will be rised.
        uuid.UUID(filename)

        self.assertEqual(extension, 'jpg')

    def test_save_method_with_make_thumbnails(self):
        test_media_location = 'test_media'

        if not os.path.exists(test_media_location):
            os.mkdir(test_media_location)

        ProductImage.image_large.field.storage.location = test_media_location

        try:
            image = Image.new('RGB', (600, 912))
            image_file = os.path.join(test_media_location, 'image_file.jpg')
            image.save(image_file)

            with open(image_file, 'rb') as f:
                product = Product.objects.get(id=1)

                product_image = ProductImage(
                    product=product, image_large=File(f))
                product_image.save()

            def get_image_size(filename):
                img = Image.open(os.path.join(test_media_location, filename))
                return img.size

            self.assertEqual(get_image_size(
                product_image.image_large.name), (600, 912))

            _, image_medium_height = get_image_size(
                product_image.image_medium.name)
            self.assertEqual(image_medium_height, 466)

            _, image_small_height = get_image_size(
                product_image.image_small.name)
            self.assertEqual(image_small_height, 124)

        finally:
            if os.path.exists(test_media_location):
                shutil.rmtree(test_media_location)


class ProductItemModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(
            name='Test category name')
        product = Product.objects.create(
            category=category, name='Test product name')

        ProductItem.objects.create(product=product)

    def test_product_label(self):
        product_item = ProductItem.objects.get(id=1)
        field_label = product_item._meta.get_field('product').verbose_name
        self.assertEqual(field_label, 'product')

    def test_product_field_related_model(self):
        product_item = ProductItem.objects.get(id=1)
        related_model = product_item._meta.get_field('product').related_model
        self.assertEqual(related_model, Product)

    def test_product_field_related_name(self):
        product_item = ProductItem.objects.get(id=1)
        related_name = product_item._meta.get_field(
            'product').remote_field.related_name
        self.assertEqual(related_name, 'product_items')

    def test_product_field_on_detele(self):
        product_item = ProductItem.objects.get(id=1)
        on_detele = product_item._meta.get_field(
            'product').remote_field.on_delete
        self.assertEqual(on_detele, models.CASCADE)

    def test_size_label(self):
        product_item = ProductItem.objects.get(id=1)
        field_label = product_item._meta.get_field('size').verbose_name
        self.assertEqual(field_label, 'size')

    def test_size_default(self):
        product_item = ProductItem.objects.get(id=1)
        default = product_item._meta.get_field('size').default
        self.assertEqual(default, 48)

    def test_quantity_label(self):
        product_item = ProductItem.objects.get(id=1)
        field_label = product_item._meta.get_field('quantity').verbose_name
        self.assertEqual(field_label, 'quantity')

    def test_quantity_default(self):
        product_item = ProductItem.objects.get(id=1)
        default = product_item._meta.get_field('quantity').default
        self.assertEqual(default, 0)

    def test_object_name_is_product_name_colon_size_colon_quantity(self):
        product_item = ProductItem.objects.get(id=1)
        expected_object_name = f'{product_item.product.name} : {product_item.size} : {product_item.quantity}'
        self.assertEqual(str(product_item), expected_object_name, )
