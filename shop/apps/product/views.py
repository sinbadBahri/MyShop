from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .models import Category, Brand, Product
from .serializers import CategorySerializer, BrandSerializer, ProductSerializer


class CategoryViewSet(viewsets.ViewSet):
    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer)
    def list(self, request) -> Response:
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)


class BrandViewSet(viewsets.ViewSet):
    queryset = Brand.objects.all()

    @extend_schema(responses=BrandSerializer)
    def list(self, request) -> Response:
        serializer = BrandSerializer(self.queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):
    queryset = Product.objects.all()

    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=["get"],
        detail=False,
        url_path=r"category/(?P<category>\w+)/all",
        url_name="all",
    )
    def list_product_by_category(self, request, category=None):
        """
        An endpoint to return products by category
        """
        serializer = ProductSerializer(
            self.queryset.filter(category__title=category),
            many=True,
        )
        return Response(serializer.data)