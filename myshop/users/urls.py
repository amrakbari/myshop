from django.urls import path
from .apis import ProfileApi, RegisterApi, ActivateApiView

urlpatterns = [
    path('register/', RegisterApi.as_view(), name="register"),
    path('activate/<str:uidb64>/<str:token>/', ActivateApiView.as_view(), name="activate"),
    path('profile/', ProfileApi.as_view(), name="profile"),
]
1