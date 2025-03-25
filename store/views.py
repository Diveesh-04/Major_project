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
import razorpay
from django.conf import settings
from razorpay.errors import BadRequestError, SignatureVerificationError 


from .models import Category, Product, Cart, Order
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
    
    
def shop_view(request):
    selected_categories = Category.objects.filter(slug__in=['attar', 'perfume', 'home-frag', 'multi-perf'])
    return render(request, 'store/base.html', {'categories': selected_categories})

# ------------------ FRONTEND VIEWS ------------------


def home(request):
    specific_categories = ["Attar", "Perfume", "Home Fragrances", "Multi Fragrances"]
    categories = Category.objects.filter(name__in=specific_categories)

    # Exclude "Multiperf" products
    products = Product.objects.filter(category__in=categories).exclude(category__name="Multi Fragrances")[:10]  

    return render(request, "store/home.html", {"categories": categories, "products": products})

  
def category_list(request, category_id=None):
    filter_param = request.GET.get("filter")  # Get filter from URL

    if filter_param == "him":
        category = get_object_or_404(Category, name__icontains="Him")
        products = Product.objects.filter(category=category)
        return render(request, "store/category.html", {"category": category, "products": products})

    elif filter_param == "her":
        category = get_object_or_404(Category, name__icontains="Her")
        products = Product.objects.filter(category=category)
        return render(request, "store/category.html", {"category": category, "products": products})

    elif filter_param == "perfume":
        categories = Category.objects.filter(name__icontains="Perfume")  # Get all categories matching "Perfume"
        products = Product.objects.filter(category__in=categories)  # Fetch products for all matching categories
        return render(request, "store/category.html", {"categories": categories, "products": products})

    elif category_id:
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category)
        return render(request, "store/category.html", {"category": category, "products": products})

    categories = Category.objects.all()
    return render(request, "store/categories.html", {"categories": categories})


def category_page(request):
    filter_param = request.GET.get("filter", "")  # Default to an empty string if no filter is provided

    if filter_param.lower() == "him":
        categories = Category.objects.filter(name__icontains="Him")
    elif filter_param.lower() == "her":
        categories = Category.objects.filter(name__icontains="Her")
    else:
        categories = Category.objects.all()

    return render(request, "category_page.html", {"categories": categories})
    
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


# ------------------ ORDER FUNCTIONALITIES ------------------

def create_razorpay_order(request):
    """
    Creates a Razorpay order when a user proceeds to checkout.
    """
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User must be logged in"}, status=403)

    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        return JsonResponse({"error": "Cart is empty"}, status=400)

    total_price = sum(item.product.price * item.quantity for item in cart_items)
    total_price_paise = int(total_price * 100)  # Convert to paisa

    try:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        razorpay_order = client.order.create({
            "amount": total_price_paise,
            "currency": "INR",
            "payment_capture": "1"
        })

        order = Order.objects.create(
            user=request.user,
            razorpay_order_id=razorpay_order["id"],
            total_price=total_price,
            status="Pending"
        )

        return JsonResponse({
            "order_id": razorpay_order["id"],
            "total_price": total_price,
            "razorpay_key": settings.RAZORPAY_KEY_ID
        })

    except razorpay.errors.BadRequestError as e:
        return JsonResponse({"error": f"Razorpay Error: {str(e)}"}, status=400)


@csrf_exempt
def payment_success(request):
    """
    Verifies the Razorpay payment and updates the order status.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            razorpay_order_id = data.get("razorpay_order_id")
            razorpay_payment_id = data.get("razorpay_payment_id")
            razorpay_signature = data.get("razorpay_signature")

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            params_dict = {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature
            }

            client.utility.verify_payment_signature(params_dict)

            # Update order status
            order = get_object_or_404(Order, razorpay_order_id=razorpay_order_id)
            order.status = "Paid"
            order.save()

            return JsonResponse({"status": "success", "message": "Payment verified"})

        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({"error": "Signature verification failed"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


# ------------------ CHECKOUT FUNCTION ------------------

def checkout(request):
    
   
   
    if not request.user.is_authenticated:
        return redirect("login")

    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        return render(request, "store/checkout.html", {"error": "Cart is empty"})

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, "store/checkout.html", {
        "cart_items": cart_items,
        "total_price": total_price,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
    })


# ------------------ ORDER SUCCESS PAGE ------------------

def order_success(request):
    """
    Displays a success page after a successful payment.
    """
    return render(request, "store/order_success.html")


# ------------------ LOGIN MODAL ------------------

def login_modal(request):
    return render(request, 'store/login_modal.html')


