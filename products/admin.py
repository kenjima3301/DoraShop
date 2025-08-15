from django.contrib import admin
from .models import Comic
from django.utils.html import format_html

@admin.register(Comic)
class ComicAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "price", "thumbnail")

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="90" />', obj.image.url)
        return "-"
    thumbnail.short_description = "Ảnh bìa"
