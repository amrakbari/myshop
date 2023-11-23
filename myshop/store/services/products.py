from django.db.models import QuerySet

from myshop.store.models import Product


def create_product(name: str, description: str, price: float, image) -> QuerySet[Product]:
    queryset = Product.objects.create(
        name=name,
        description=description,
        price=price,
        image=image,
    )
    return queryset
