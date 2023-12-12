from django.db import models

from myshop.common.models import BaseModel
from myshop.users.models import BaseUser


class Address(BaseModel):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    address = models.TextField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)


class Store(BaseModel):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)


# Create your models here.
class Product(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
