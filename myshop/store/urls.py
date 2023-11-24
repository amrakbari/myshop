from django.urls import path, include

from myshop.store.apis.products import ProductApi
from myshop.store.apis.product_image import ProductImageApi

urlpatterns = [
    path('products/', ProductApi.as_view()),
    path('products/<int:product_id>/image/', ProductImageApi.as_view()),
]
