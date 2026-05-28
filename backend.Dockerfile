# ============================================
# DOCKERFILE - BACKEND DJANGO
# ============================================

FROM python:3.11-slim

# Variables de entorno para Python
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema para PostgreSQL y cryptography
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    python3-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código del backend
COPY backend/ .

# Exponer puerto Django
EXPOSE 8000

# Script de inicio con espera de base de datos, migraciones y carga de datos
CMD sh -c 'until pg_isready -h ${DB_HOST} -p ${DB_PORT} -U ${DB_USER}; do \
      echo "Waiting for database..."; \
      sleep 2; \
    done && \
    echo "Database is ready!" && \
    python manage.py migrate --fake-initial --noinput && \
    python manage.py seed_all && \
    python manage.py runserver 0.0.0.0:8000'
