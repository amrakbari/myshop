from rest_framework import serializers

from myshop.store.models import Product


class ProductInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)


class ProductOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
