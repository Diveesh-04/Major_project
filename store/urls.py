from django.urls import path, include
from rest_framework.routers import DefaultRouter  
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth.views import LogoutView
from .views import (
    CategoryViewSet, 
    ProductViewSet, 
    CartViewSet, 
    RegisterView, 
    CustomTokenObtainPairView, 
    home, 
    cart_view,
    category_list,
    product_detail
)

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'cart', CartViewSet)

# Define URL patterns
urlpatterns = [
    # API Endpoints
    path('api/', include(router.urls)),  
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Authentication & Logout
    path('logout/', LogoutView.as_view(), name='logout'),

    # Frontend Views
    path('', home, name='home'),  # Homepage
    path('categories/', category_list, name='category_list'),  # Category listing
    path('category/<int:category_id>/', category_list, name='category_page'),  # Category detail
     path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('cart/', cart_view, name='cart'),  # Cart Page (Fix for NoReverseMatch error)
]