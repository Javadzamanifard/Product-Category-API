from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import ProductApiView


router = DefaultRouter()
router.register(r'product', ProductApiView, basename='product')
# urlpatterns = router.urls
urlpatterns = [
    path('api/', include(router.urls))
]


