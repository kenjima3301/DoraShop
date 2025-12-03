from django.shortcuts import render, get_object_or_404, redirect
from .models import Comic
from django.http import HttpResponse
from django.contrib.auth import logout

def comic_list(request):
    comics = Comic.objects.all()
    return render(request, 'products/comic_list.html', {'comics': comics})

def home(request):
    featured_comics = Comic.objects.all()[:8] 
    return render(request, 'home.html', {'featured_comics': featured_comics})

def product_list(request):
    comics = Comic.objects.all()
    return render(request, 'products/list.html', {'comics': comics})

def product_detail(request, pk):
    comic = get_object_or_404(Comic, pk=pk)
    return render(request, 'products/detail.html', {'comic': comic})


# --- NHÓM GIỎ HÀNG (Cart) ---
# (Sau này nên chuyển sang app 'cart')

def cart_summary(request):
    """Hiển thị trang giỏ hàng (cart/summary.html)"""
    return render(request, 'cart/summary.html')


# --- NHÓM TÀI KHOẢN (Auth) ---
# (Sau này nên chuyển sang app 'accounts' hoặc dùng Django Auth có sẵn)

def login_view(request):
    return render(request, 'auth/login.html')

def register_view(request):
    return render(request, 'auth/register.html')

def logout_view(request):
    logout(request)
    return redirect('home')