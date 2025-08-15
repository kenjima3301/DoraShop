from django.shortcuts import render
from .models import Comic

def comic_list(request):
    comics = Comic.objects.all()
    return render(request, 'products/comic_list.html', {'comics': comics})
