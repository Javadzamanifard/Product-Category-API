from rest_framework.viewsets import ModelViewSet

from serializers import CategorySerializer, ProductSerializer

from models import Category, Product

from .pagination import DefaultPagination

from django.db.models import Q


class CategoryApiView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = DefaultPagination


class ProductApiView(ModelViewSet):
    serializer_class = ProductSerializer
    pagination_class = DefaultPagination
    
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