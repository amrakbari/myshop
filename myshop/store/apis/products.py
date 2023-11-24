from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from myshop.store.serializers import ProductInputSerializer, ProductOutputSerializer
from myshop.store.services.products import create_product


class ProductApi(APIView):

    @extend_schema(request=ProductInputSerializer, responses=ProductOutputSerializer)
    def post(self, request):
        input_serializer = ProductInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        try:
            query = create_product(
                input_serializer.validated_data.get('name'),
                input_serializer.validated_data.get('description'),
                input_serializer.validated_data.get('price'),
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(ProductOutputSerializer(query, context={"request": request}).data,
                        status=status.HTTP_201_CREATED)

    def get(self, request):
        ...
