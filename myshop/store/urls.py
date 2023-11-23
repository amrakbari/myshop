from django.urls import path, include

from myshop.store.apis.products import ProductApi

urlpatterns = [
    path('products/', ProductApi.as_view())
]
