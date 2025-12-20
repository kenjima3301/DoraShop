from .models import Cart


def cart_context(request):
    """Context processor để hiển thị số lượng sản phẩm trong giỏ hàng"""
    cart_count = 0
    
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = cart.get_cart_count()
        except Cart.DoesNotExist:
            cart_count = 0
    
    return {
        'cart_count': cart_count
    }
