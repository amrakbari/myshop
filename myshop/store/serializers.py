from rest_framework import serializers


class ProductInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500)
    price = serializers.IntegerField()
    image = serializers.ImageField()
