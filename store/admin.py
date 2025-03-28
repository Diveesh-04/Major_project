from django.contrib import admin
from .models import CustomUser, Category, Product, Cart, Order

admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Product)

admin.site.register(Order) 
class CartAdmin(admin.ModelAdmin):
    list_display = ('user_display', 'product', 'quantity', 'created_at')
    search_fields = ('user__username', 'session_id', 'product__name')
    list_filter = ('created_at', 'user')

    def user_display(self, obj):
        return obj.user.username if obj.user else f"Guest ({obj.session_id})"
    user_display.short_description = 'User'

admin.site.register(Cart, CartAdmin)

