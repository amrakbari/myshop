from django.db.models import QuerySet

from myshop.store.models import Product


def get_products() -> QuerySet[Product]:
    return Product.objects.all()