from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('total_price',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at', 'get_total')
    inlines = [CartItemInline]
    
    def get_total(self, obj):
        return f"{obj.get_cart_total():.0f}đ"
    get_total.short_description = 'Tổng giá trị'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'comic', 'quantity', 'total_price')
    list_filter = ('cart__user',)
