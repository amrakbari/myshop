from django.urls import path, include

urlpatterns = [
    path('users/', include(('myshop.users.urls', 'users'))),
    path('store/', include(('myshop.store.urls', 'store')))
]
