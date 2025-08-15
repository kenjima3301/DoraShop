# Base image
FROM python:3.11-slim

# Env settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y netcat-openbsd

# Work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

COPY ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh

# Collect static files (for production)
RUN python manage.py collectstatic --noinput

ENTRYPOINT ["/app/entrypoint.sh"]

# Default command
CMD ["gunicorn", "dorashop.wsgi:application", "--bind", "0.0.0.0:8000"]
