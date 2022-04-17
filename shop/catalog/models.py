import os

from io import BytesIO
from PIL import Image
from uuid import uuid4

from django.core.files import File
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    slug = models.SlugField(unique=True, db_index=True)
    sort = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort']

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, db_index=True)
    description = models.TextField()
    detail = models.TextField()
    price = models.PositiveIntegerField(default=0)
    discount = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def new_price(self):
        if self.discount > 0:
            return self.price - self.price * self.discount // 100
        return self.price

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    def get_file_path(self, filename):
        extension = filename.split('.')[-1]
        filename = f'{uuid4()}.{extension}'
        return os.path.join("product_images", filename)

    product = models.ForeignKey(
        Product, related_name='product_images', on_delete=models.CASCADE)
    image_large = models.ImageField(
        verbose_name='Large image', upload_to=get_file_path, max_length=255, blank=True, null=True)
    image_medium = models.ImageField(
        verbose_name='Medium image', upload_to=get_file_path, max_length=255, blank=True, null=True)
    image_small = models.ImageField(
        verbose_name='Small image', upload_to=get_file_path, max_length=255, blank=True, null=True)
    sort = models.IntegerField(default=0)

    class Meta:
        ordering = ['product__name', 'sort']

    def save(self, *args, **kwargs):
        if self.image_large:
            self.image_medium = self.make_thumbnail(
                self.image_large, (310, 466))
            self.image_small = self.make_thumbnail(self.image_large, (85, 124))

        super(ProductImage, self).save(*args, **kwargs)

    @staticmethod
    def make_thumbnail(image, size):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=95)

        thumbnail = File(thumb_io, name=image.name)
        return thumbnail

    def __str__(self):
        return self.product.name


class ProductItem(models.Model):
    SIZE_CHOICES = [
        (48, 48),
        (50, 50),
        (52, 52),
        (54, 54),
        (56, 56),
        (58, 58),
        (60, 60)
    ]

    product = models.ForeignKey(
        Product, related_name='product_items', on_delete=models.CASCADE)
    size = models.IntegerField(choices=SIZE_CHOICES, default=48)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.product.name} : {self.size} : {self.quantity}'
