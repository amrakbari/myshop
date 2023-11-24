from django.db.models import QuerySet

from myshop.store.models import Product


def create_product(name: str, description: str, price: float,) -> QuerySet[Product]:
    queryset = Product.objects.create(
        name=name,
        description=description,
        price=price,
    )
    return queryset
