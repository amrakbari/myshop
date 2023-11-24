from django.db.models import QuerySet

from myshop.store.models import Product


def create_product(name: str, description: str, price: float, ) -> QuerySet[Product]:
    queryset = Product.objects.create(
        name=name,
        description=description,
        price=price,
    )
    return queryset


def create_product_image(product_id: int, image: str) -> QuerySet[Product]:
    product = Product.objects.get(id=product_id)
    product.image = image
    product.save()
    return product
