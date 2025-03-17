from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt
from .models import Category, Product, Cart
import json
from .models import Product
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

# Cart ViewSet - Fetch cart items for the logged-in user
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()  
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

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
    categories = Category.objects.all()  
    return render(request, 'store/home.html', {'categories': categories})

# Cart Page View - Show items in the cart
def view_cart(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = Cart.objects.filter(session_id=request.session.session_key)
    
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price})


# Add to Cart View (Supports Logged-in Users & Guests)
def add_to_cart(request, product_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            quantity = data.get('quantity', 1)

            product = Product.objects.get(id=product_id)

            if request.user.is_authenticated:
                cart_item, created = Cart.objects.get_or_create(
                    user=request.user,
                    product=product,
                    defaults={'quantity': quantity}
                )
            else:
                session_id = request.session.session_key
                if not session_id:
                    request.session.create()
                    session_id = request.session.session_key

                cart_item, created = Cart.objects.get_or_create(
                    session_id=session_id,
                    product=product,
                    defaults={'quantity': quantity}
                )

            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            return JsonResponse({'message': 'Added to cart', 'cartItemId': cart_item.id})

        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


   
def view_cart(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        session_id = request.session.session_key
        cart_items = Cart.objects.filter(session_id=session_id)

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price})

def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)  # Adjust query if needed
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'store/checkout.html', {'cart_items': cart_items, 'total_price': total_price})


# Remove from Cart View
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    cart_item.delete()
    return redirect('view_cart')

# Category Page View
def category_list(request, category_id=None):
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category)
        return render(request, 'store/category.html', {'category': category, 'products': products})
    else:
        categories = Category.objects.all()
        return render(request, 'store/categories.html', {'categories': categories})

# Product Detail View
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

# About Page View
def about(request):
    return render(request, 'store/about.html')


