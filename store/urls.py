from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter  
from rest_framework_simplejwt.views import TokenRefreshView
from .views import register, login_user, logout_user
from . import views 
from .views import (
    CategoryViewSet, 
    ProductViewSet, 
    CartViewSet, 
    RegisterView, 
    CustomTokenObtainPairView, 
    home, 
    category_list,
    product_detail,
    add_to_cart,
    view_cart,
    remove_from_cart,
    about,
    checkout,
    update_cart_quantity,
)

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'cart', CartViewSet,basename='cart')  # Cart API

# Define URL patterns
urlpatterns = [
    # API Endpoints
    path('api/', include(router.urls)),  
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
      # Cart API
    path('api/cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),  # ✅ API Add to Cart
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
      path('update-cart-quantity/', update_cart_quantity, name='update_cart_quantity'),

    # Frontend Views
    path('cart/', view_cart, name='cart'),  # ✅ Cart Page
    path('checkout/',  views.checkout, name='checkout'),
    
    # Authentication & Logout
   path("register/", register, name="register"),
    path("login/", login_user, name="login"),
     path('logout/', logout_user, name='logout'),

    # Frontend Views
    path('', home, name='home'),  # Homepage
    path('categories/', category_list, name='category_list'),  # Category listing
    path('category/<int:category_id>/', category_list, name='category_page'),  # Category detail
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    
    # Cart URLs
    path('cart/', view_cart, name='view_cart'),  # ✅ Fixed "view_cart" name
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),  # Add to Cart
    path('cart/remove/<int:cart_id>/', remove_from_cart, name='remove_from_cart'),  # Remove from Cart

    # About Page
    path('about/', about, name='about'),
]

# ✅ Serve media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)                        