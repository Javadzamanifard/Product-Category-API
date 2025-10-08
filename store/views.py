from rest_framework.viewsets import ModelViewSet

from serializers import CategorySerializer, ProductSerializer

from models import Category, Product


class CategoryApiView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductApiView(ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
