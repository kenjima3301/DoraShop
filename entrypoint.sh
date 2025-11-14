#!/bin/sh

# Dừng ngay lập tức nếu bất kỳ lệnh nào thất bại
set -e

# In ra thông báo và bắt đầu vòng lặp chờ database
echo "Waiting for database to be ready..."

# Biến DB_HOST được lấy từ docker-compose.yml
# Lệnh 'nc -z' (netcat) sẽ kiểm tra xem cổng 5432 trên host đó có mở không.
# Vòng lặp sẽ tiếp tục cho đến khi cổng sẵn sàng.
while ! nc -z $DB_HOST 5432; do
  sleep 1
done

echo "Database is ready!"

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Chạy migrations của Django
echo "Applying database migrations..."
python manage.py migrate

# docker-compose exec web python manage.py createsuperuser

# 'exec "$@"' là một lệnh đặc biệt.
# "$@" đại diện cho tất cả các đối số được truyền vào script.
# Trong trường hợp này, nó chính là lệnh CMD từ Dockerfile:
# ["gunicorn", "dorashop.wsgi:application", "--bind", "0.0.0.0:8000"]
# 'exec' sẽ thay thế tiến trình của script bằng tiến trình gunicorn,
# đây là cách làm đúng chuẩn để chạy ứng dụng chính.
exec "$@"