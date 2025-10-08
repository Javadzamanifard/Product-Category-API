from rest_framework.viewsets import ModelViewSet

from serializers import CategorySerializer, ProductSerializer

from models import Category, Product

from .pagination import DefaultPagination


class CategoryApiView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = DefaultPagination


class ProductApiView(ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    pagination_class = DefaultPagination
