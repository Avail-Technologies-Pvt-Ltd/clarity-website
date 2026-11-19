# syntax=docker/dockerfile:1.4
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies (curl for healthchecks, netcat for db polling, build-essential for C extensions)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libpq-dev \
    libpq5 \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements-docker.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-docker.txt

# Copy application code
COPY . /app/

# Ensure directories for static, media, data, and logs exist
RUN mkdir -p /app/staticfiles /app/media /app/data /app/logs /app/tmp

# BUILD_HASH is injected at build time (e.g. git commit sha)
ARG BUILD_HASH=unknown
ENV APP_BUILD_HASH=${BUILD_HASH}

ENV DJANGO_SETTINGS_MODULE=clarity_website.settings_prod
ENV PYTHONUNBUFFERED=1
ENV DEBUG=False

# Run collectstatic at build time for instant startup
RUN SECRET_KEY="build-time-static-collection-key" python manage.py collectstatic --noinput --settings=clarity_website.settings_dev

# Normalize entrypoint line endings and make executable
RUN sed -i 's/\r$//' /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Create non-root user for security and grant permissions
RUN useradd -m clarityuser && chown -R clarityuser:clarityuser /app && chmod -R 775 /app/media /app/logs /app/data /app/staticfiles
USER clarityuser

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1

ENTRYPOINT ["/app/entrypoint.sh"]

# Launch with Gunicorn WSGI server
CMD ["gunicorn", "clarity_website.wsgi:application", "--bind", "0.0.0.0:8000", "--timeout", "120"]
