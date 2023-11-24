from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView, status
from rest_framework.parsers import MultiPartParser

from rest_framework.response import Response

from myshop.store.services.products import create_product_image
from myshop.store.serializers import ProductOutputSerializer, ProductImageInputSerializer


class ProductImageApi(APIView):
    parser_classes = [MultiPartParser]

    @extend_schema(
        request=ProductImageInputSerializer,
        responses=ProductOutputSerializer,
    )
    def post(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        file = request.data.get('file')
        if not file:
            return Response({'error': 'No file found'}, status=status.HTTP_400_BAD_REQUEST)
        query_set = create_product_image(product_id, file)
        return Response(ProductOutputSerializer(query_set, context={"request": request}).data,
                        status=status.HTTP_201_CREATED)
