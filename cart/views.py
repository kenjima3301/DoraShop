from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Cart, CartItem
from products.models import Comic


def get_or_create_cart(user):
    """Helper function để lấy hoặc tạo cart cho user"""
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


@login_required
def cart_summary(request):
    """Hiển thị trang giỏ hàng"""
    cart = get_or_create_cart(request.user)
    cart_items = cart.items.select_related('comic').all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'cart_total': cart.get_cart_total(),
    }
    return render(request, 'cart/summary.html', context)


@login_required
def cart_add(request, comic_id):
    """Thêm sản phẩm vào giỏ hàng"""
    comic = get_object_or_404(Comic, id=comic_id)
    cart = get_or_create_cart(request.user)
    
    # Lấy số lượng từ POST request, mặc định là 1
    quantity = int(request.POST.get('quantity', 1))
    
    # Check stock
    if comic.stock < quantity:
        messages.error(request, f'Không đủ hàng! Chỉ còn {comic.stock} cuốn.')
        return redirect('product_detail', pk=comic_id)
    
    # Thêm hoặc cập nhật cart item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        comic=comic,
        defaults={'quantity': quantity}
    )
    
    if not created:
        # Nếu đã có trong giỏ, tăng số lượng
        new_quantity = cart_item.quantity + quantity
        if new_quantity > comic.stock:
            messages.error(request, f'Không đủ hàng! Chỉ còn {comic.stock} cuốn.')
            return redirect('cart:summary')
        cart_item.quantity = new_quantity
        cart_item.save()
        messages.success(request, f'Đã cập nhật số lượng "{comic.title}" trong giỏ hàng!')
    else:
        messages.success(request, f'Đã thêm "{comic.title}" vào giỏ hàng!')
    
    return redirect('cart:summary')


@login_required
def cart_remove(request, item_id):
    """Xóa sản phẩm khỏi giỏ hàng"""
    cart = get_or_create_cart(request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    comic_title = cart_item.comic.title
    cart_item.delete()
    
    messages.success(request, f'Đã xóa "{comic_title}" khỏi giỏ hàng!')
    return redirect('cart:summary')


@login_required
def cart_update(request, item_id):
    """Cập nhật số lượng sản phẩm trong giỏ"""
    if request.method == 'POST':
        cart = get_or_create_cart(request.user)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity <= 0:
            cart_item.delete()
            messages.success(request, 'Đã xóa sản phẩm khỏi giỏ hàng!')
        elif quantity > cart_item.comic.stock:
            messages.error(request, f'Không đủ hàng! Chỉ còn {cart_item.comic.stock} cuốn.')
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Đã cập nhật số lượng!')
    
    return redirect('cart:summary')


@login_required
def cart_clear(request):
    """Xóa toàn bộ giỏ hàng"""
    cart = get_or_create_cart(request.user)
    cart.items.all().delete()
    messages.success(request, 'Đã xóa toàn bộ giỏ hàng!')
    return redirect('cart:summary')
