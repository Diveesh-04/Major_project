from rest_framework import serializers
from .models import Category, Product, Cart

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'  # Serialize all fields

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # Include category details in product response

    class Meta:
        model = Product
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  # Include product details in cart response

    class Meta:
        model = Cart
        fields = '__all__'