from rest_framework import serializers

from catalog.models import Category, Product, ProductItem, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description',
            'slug'
        ]


class ProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductItem
        fields = [
            'id',
            'size',
            'quantity'
        ]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = [
            'id',
            'image_large',
            'image_medium',
            'image_small'
        ]


class ProductSerializer(serializers.ModelSerializer):
    product_items = ProductItemSerializer(many=True, read_only=True)
    product_images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
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
        ]
