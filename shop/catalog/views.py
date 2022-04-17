from django.http import Http404

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from catalog.models import Category, Product
from catalog.serializers import CategorySerializer, ProductSerializer
from catalog.pagination import ProductPagination


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'categories': reverse('category-list', request=request, format=format)
    })


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None


class ProductList(APIView, ProductPagination):
    def get(self, request, category_slug):
        try:
            category = Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404

        products = Product.objects.filter(
            category__slug=category_slug, product_items__quantity__gt=0
        ).distinct()

        results = self.paginate_queryset(products, request, view=self)
        product_serializer = ProductSerializer(
            results, context={"request": request}, many=True)
        category_serializer = CategorySerializer(category)

        return self.get_paginated_response(product_serializer.data, category_serializer.data)


class ProductDetail(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']

        return Product.objects.filter(category__slug=category_slug)
