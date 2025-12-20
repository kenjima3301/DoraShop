from django.shortcuts import render, get_object_or_404, redirect
from .models import Comic
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm

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
    # Lấy 4 truyện ngẫu nhiên khác để recommend
    related_comics = Comic.objects.exclude(pk=pk).order_by('?')[:4]
    return render(request, 'products/detail.html', {
        'comic': comic,
        'related_comics': related_comics
    })


# --- AUTHENTICATION VIEWS ---

def login_view(request):
    """Xử lý đăng nhập"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Chào mừng {username}!')
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng!')
    else:
        form = UserLoginForm()
    
    return render(request, 'auth/login.html', {'form': form})


def register_view(request):
    """Xử lý đăng ký tài khoản mới"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Tài khoản {username} đã được tạo thành công!')
            login(request, user)
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = UserRegisterForm()
    
    return render(request, 'auth/register.html', {'form': form})


def logout_view(request):
    """Đăng xuất"""
    logout(request)
    messages.info(request, 'Bạn đã đăng xuất!')
    return redirect('home')