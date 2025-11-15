# ~/DoraShop/products/management/commands/create_admin.py

import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

# Lấy mô hình User (người dùng)
User = get_user_model()

class Command(BaseCommand):
    """
    Lệnh Django này sẽ tạo một superuser (admin)
    một cách không tương tác (non-interactively) nếu nó chưa tồn tại.

    Đọc thông tin từ file .env (Biến Môi trường)
    """
    help = "Tạo admin từ các biến môi trường (env variables)"

    def handle(self, *args, **options):
        # Lấy thông tin từ file .env
        username = os.environ.get('DJANGO_ADMIN_USER')
        email = os.environ.get('DJANGO_ADMIN_EMAIL')
        password = os.environ.get('DJANGO_ADMIN_PASSWORD')

        # --- LOGIC "IDEMPOTENT" (Quan trọng) ---
        # Kiểm tra xem user đã tồn tại chưa
        if not User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(f'Đang tạo tài khoản admin: {username}'))

            # Tạo superuser
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'Tạo admin "{username}" thành công!'))
        else:
            self.stdout.write(self.style.WARNING(f'Admin "{username}" đã tồn tại, bỏ qua.'))
