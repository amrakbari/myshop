from django.urls import path, include

urlpatterns = [
    path('store/', include(('myshop.store.urls', 'store')))
]
