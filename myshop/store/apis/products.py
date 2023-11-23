from rest_framework.views import APIView

from myshop.store.serializers import ProductInputSerializer


class ProductApi(APIView):
    __input_serializer_instance = ProductInputSerializer()

    def post(self, request):
        ...

    def get(self, request):
        ...
