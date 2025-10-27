from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import CustomUserViewset, ProductApiView


router = DefaultRouter()
router.register(r'product', ProductApiView, basename='product')
router.register(r'customers', CustomUserViewset, basename='customer')
# urlpatterns = router.urls
urlpatterns = [
    path('', include(router.urls)),
]


