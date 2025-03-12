from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Cart
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    CartSerializer,
    CustomUserSerializer,
    CustomTokenObtainPairSerializer,
)

User = get_user_model()

# Category ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

# Product ViewSet
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

# Cart ViewSet
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

# User Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Login View with JWT
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Home View
def home(request):
    categories = Category.objects.all()  # Fetch all categories
    return render(request, 'store/home.html', {'categories': categories})

# Cart Page View
def cart_view(request):
    return render(request, 'store/cart.html')

# Category Page View

def category_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)  # Fetch the category safely
    products = Product.objects.filter(category=category)  # Get products for this category
    return render(request, 'store/category.html', {'category': category, 'products': products})


# Product Detail View
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})