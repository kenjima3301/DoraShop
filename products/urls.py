from django.urls import path
from .views import comic_list

urlpatterns = [
    path('', comic_list, name='comic_list'),
]
