from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from myshop.api.pagination import LimitOffsetPagination
from myshop.store.models import Product
from myshop.store.selectors.products import get_products
from myshop.store.serializers import ProductInputSerializer, ProductOutputSerializer
from myshop.store.services.products import create_product


class ProductApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 15

    @extend_schema(request=ProductInputSerializer, responses=ProductOutputSerializer)
    def post(self, request):
        input_serializer = ProductInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        try:
            query_set = create_product(
                input_serializer.validated_data.get('name'),
                input_serializer.validated_data.get('description'),
                input_serializer.validated_data.get('price'),
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(ProductOutputSerializer(query_set, context={"request": request}).data,
                        status=status.HTTP_201_CREATED)

    @extend_schema(responses=ProductOutputSerializer)
    def get(self, request):
        query_set = get_products()
        return Response(ProductOutputSerializer(query_set, context={"request": request}, many=True).data,
                        status=status.HTTP_200_OK)
