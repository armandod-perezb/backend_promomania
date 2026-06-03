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

# Dar permisos al entrypoint
RUN chmod +x /app/entrypoint.sh

# Exponer puerto Django
EXPOSE 8000

# Comando por defecto para producción (Render usará este)
CMD ["/app/entrypoint.sh"]
