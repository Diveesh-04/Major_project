from django.urls import path, include
from rest_framework.routers import DefaultRouter  
from .views import CategoryViewSet, ProductViewSet, CartViewSet

# Create a router
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'cart', CartViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # Include API URLs
]