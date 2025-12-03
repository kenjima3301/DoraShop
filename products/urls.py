from django.urls import path
from .views import comic_list, home
from . import views

urlpatterns = [
    path('test-home/', comic_list, name='comic_list'),
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_summary, name='cart_summary'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
