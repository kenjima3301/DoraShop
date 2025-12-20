from django.db import models
from django.contrib.auth.models import User
from products.models import Comic


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def get_cart_total(self):
        """Tính tổng giá trị giỏ hàng"""
        return sum(item.total_price() for item in self.items.all())

    def get_cart_count(self):
        """Đếm tổng số sản phẩm trong giỏ"""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'comic')

    def __str__(self):
        return f"{self.quantity}x {self.comic.title}"

    def total_price(self):
        """Tính tổng giá của item này"""
        return self.comic.price * self.quantity
