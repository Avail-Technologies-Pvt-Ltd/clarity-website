# settings_prod.py — clarity_website
# Production settings for AWS EC2 / Docker deployment
from .settings import *
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = [h.strip() for h in config('ALLOWED_HOSTS', default='*').split(',') if h.strip()]

# CSRF Trusted Origins
csrf_env = config('CSRF_TRUSTED_ORIGINS', default='')
if csrf_env:
    CSRF_TRUSTED_ORIGINS = [o.strip() for o in csrf_env.split(',') if o.strip()]
else:
    # Auto-allow HTTP/HTTPS for hosts listed in ALLOWED_HOSTS if not wildcard
    CSRF_TRUSTED_ORIGINS = ['http://localhost', 'http://127.0.0.1']
    for host in ALLOWED_HOSTS:
        if host not in ['*', 'localhost', '127.0.0.1']:
            CSRF_TRUSTED_ORIGINS.extend([f"http://{host}", f"https://{host}"])

# Database configuration (Postgres default, supports SQLite fallback via SQLITE_PATH or DB_ENGINE)
DB_ENGINE = config('DB_ENGINE', default='postgresql')
SQLITE_PATH = config('SQLITE_PATH', default='')

if DB_ENGINE == 'sqlite3' or SQLITE_PATH:
    sqlite_file = SQLITE_PATH or str(BASE_DIR / 'data' / 'db.sqlite3')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': sqlite_file,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='clarity_website'),
            'USER': config('DB_USER', default='website_user'),
            'PASSWORD': config('DB_PASSWORD', default='password'),
            'HOST': config('DB_HOST', default='db'),
            'PORT': config('DB_PORT', default='5432'),
            'CONN_MAX_AGE': config('CONN_MAX_AGE', default=600, cast=int),
        }
    }

# Security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)
