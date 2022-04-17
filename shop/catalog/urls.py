from django.urls import path

from catalog.views import api_root, CategoryList, ProductList, ProductDetail

urlpatterns = [
    path('', api_root),
    path('categories/',
         CategoryList.as_view(), name='category-list'),
    path('categories/<slug:category_slug>/products/',
         ProductList.as_view(), name='product-list'),
    path('categories/<slug:category_slug>/products/<slug:slug>/',
         ProductDetail.as_view(), name='product-detail'),
]
