from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt
import json
import re
from .models import Category, Product, Cart
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    CartSerializer,
    CustomUserSerializer,
    CustomTokenObtainPairSerializer,
)

User = get_user_model()

# ------------------ API VIEWS ------------------

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# ------------------ FRONTEND VIEWS ------------------

def home(request):
    categories = Category.objects.all()
    return render(request, 'store/home.html', {'categories': categories})

def category_list(request, category_id=None):
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category)
        return render(request, 'store/category.html', {'category': category, 'products': products})
    categories = Category.objects.all()
    return render(request, 'store/categories.html', {'categories': categories})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

def about(request):
    return render(request, 'store/about.html')

# ------------------ AUTHENTICATION VIEWS ------------------

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if len(username) < 3:
            messages.error(request, "Username must be at least 3 characters long.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("register")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messages.error(request, "Enter a valid email address.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return redirect("register")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("register")

        if len(password) < 8 or not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password):
            messages.error(request, "Password must be at least 8 characters long and contain letters and numbers.")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Registration successful! You can now log in.")
        return redirect("login")

    return render(request, "store/register.html")

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")
            return redirect("home")
        messages.error(request, "Invalid username or password.")
        return redirect("login")

    return render(request, "store/login.html")


def logout_user(request):
    logout(request)
    return redirect("home")  # Correctly redirecting to the home page) 

# ------------------ CART FUNCTIONALITIES ------------------

def view_cart(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart_items = Cart.objects.filter(session_id=session_id)

    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price})

def add_to_cart(request, product_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            quantity = int(data.get('quantity', 1))
            if quantity < 1:
                return JsonResponse({'error': 'Quantity must be at least 1'}, status=400)

            product = get_object_or_404(Product, id=product_id)
            
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'You must be logged in to add items to the cart.', 'redirect': '/login/'}, status=403)


            if request.user.is_authenticated:
                cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
            else:
                session_id = request.session.session_key
                if not session_id:
                    request.session.create()
                    session_id = request.session.session_key
                cart_item, created = Cart.objects.get_or_create(session_id=session_id, product=product)

            cart_item.quantity = quantity if created else cart_item.quantity + quantity
            cart_item.save()

            return JsonResponse({'message': 'Cart updated', 'cartItemId': cart_item.id, 'quantity': cart_item.quantity})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except ValueError:
            return JsonResponse({'error': 'Invalid quantity'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def update_cart_quantity(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            cart_id = data.get('cart_id')
            quantity = int(data.get('quantity', 1))
            if quantity < 1:
                return JsonResponse({'error': 'Quantity must be at least 1'}, status=400)

            cart_item = get_object_or_404(Cart, id=cart_id)
            cart_item.quantity = quantity
            cart_item.save()

            return JsonResponse({"success": True, "total_price": cart_item.product.price * cart_item.quantity})

        except (json.JSONDecodeError, ValueError):
            return JsonResponse({'error': 'Invalid data'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    cart_item.delete()
    return redirect('view_cart')

def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'store/checkout.html', {'cart_items': cart_items, 'total_price': total_price})

# ------------------ LOGIN MODAL ------------------

def login_modal(request):
    return render(request, 'store/login_modal.html')