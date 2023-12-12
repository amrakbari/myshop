from django.urls import path, include

from myshop.store.apis import ProductApi
from myshop.store.apis import ProductImageApi

urlpatterns = [
    path('products/', ProductApi.as_view()),
    path('products/<int:product_id>/image/', ProductImageApi.as_view()),
]
