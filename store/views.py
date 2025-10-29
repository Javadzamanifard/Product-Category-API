from requests import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import CategorySerializer, CustomUserSerializer, ProductSerializer

from .models import Category, CustomUser, Product

from .pagination import DefaultPagination

from django.db.models import Q

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from permissions import IsAdminOrReadOnly

class CategoryApiView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = DefaultPagination
    parser_classes = [IsAdminOrReadOnly]


class ProductApiView(ModelViewSet):
    serializer_class = ProductSerializer
    pagination_class = DefaultPagination
    permission_classes  = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        request = self.request
        user = request.user
        queryset = Product.objects.select_related('category').all()
        
        category_id = request.GET.get('category_id')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        search = request.GET.get('search', '')
        ordering = request.GET.get('ordering')
        
        if not user.is_staff:
            queryset = queryset.filter(is_active=True)
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        try:
            if min_price:
                queryset = queryset.filter(price__gte=float(min_price))
            if max_price:
                queryset = queryset.filter(price__lte=float(max_price))
        except ValueError:
            pass
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(category__name__icontains=search)
            )
        
        allowed_ordering = ['price', '-price', 'name', '-name', 'created_at', '-created_at', 'updated_at', '-updated_at']
        if ordering in allowed_ordering:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by('-created_at')
        
        return queryset


### Filtering by Django-filter
import django_filters
from django_filters.rest_framework import DjangoFilterBackend

class ProductFiter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category_id = django_filters.NumberFilter(field_name='category')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    
    class Meta:
        model = Product
        fields = ['category_id', 'min_price', 'max_price', 'name', 'is_active']


class ProductApiView(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related('category').all()
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, 'rest_framework.filters.SearchFilter', 'rest_framework.filters.OrderingFilter']
    filterset_class = ProductFiter
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['price', 'created_at', 'updated_at', 'name']
    ordering = ['-created_at']


class CustomUserViewset(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        customer, created = CustomUser.objects.get_or_create(user=request.user)
        serializer = CustomUserSerializer(customer)
        return Response(serializer.data)