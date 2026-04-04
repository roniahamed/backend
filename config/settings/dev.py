import os
from datetime import timedelta

import environ
from django.core.exceptions import ImproperlyConfigured

from .shared import *

# why: Fail-fast env loading avoids unsafe hidden defaults.
env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")


def required_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        raise ImproperlyConfigured(f"Missing required environment variable: {name}")
    return value


def parse_bool(value: str, *, name: str) -> bool:
    normalized = value.strip().lower()
    truthy = {"1", "true", "yes", "on"}
    falsy = {"0", "false", "no", "off"}
    if normalized in truthy:
        return True
    if normalized in falsy:
        return False
    raise ImproperlyConfigured(f"Invalid boolean for {name}: {value}")


SECRET_KEY = required_env("DJANGO_SECRET_KEY")
DEBUG = parse_bool(required_env("DJANGO_DEBUG"), name="DJANGO_DEBUG")
ALLOWED_HOSTS = [item.strip() for item in required_env("DJANGO_ALLOWED_HOSTS").split(",") if item.strip()]
CSRF_TRUSTED_ORIGINS = [item.strip() for item in required_env("DJANGO_CSRF_TRUSTED_ORIGINS").split(",") if item.strip()]

DATABASES = {
    "default": env.db("DATABASE_URL"),
}

CORS_ALLOWED_ORIGINS = [
    item.strip()
    for item in os.getenv(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if item.strip()
]

# why: Local memory cache keeps free-tier infra simple and fast.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": required_env("DJANGO_CACHE_LOCATION"),
    }
}

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = int(required_env("DJANGO_SECURE_HSTS_SECONDS"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = parse_bool(required_env("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS"), name="DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS")
SECURE_HSTS_PRELOAD = parse_bool(required_env("DJANGO_SECURE_HSTS_PRELOAD"), name="DJANGO_SECURE_HSTS_PRELOAD")
SESSION_COOKIE_SECURE = parse_bool(required_env("DJANGO_SESSION_COOKIE_SECURE"), name="DJANGO_SESSION_COOKIE_SECURE")
CSRF_COOKIE_SECURE = parse_bool(required_env("DJANGO_CSRF_COOKIE_SECURE"), name="DJANGO_CSRF_COOKIE_SECURE")

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(required_env("JWT_ACCESS_MINUTES"))),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(required_env("JWT_REFRESH_DAYS"))),
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = required_env("EMAIL_HOST")
EMAIL_PORT = int(required_env("EMAIL_PORT"))
EMAIL_USE_TLS = parse_bool(required_env("EMAIL_USE_TLS"), name="EMAIL_USE_TLS")
EMAIL_HOST_USER = required_env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = required_env("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = required_env("DEFAULT_FROM_EMAIL")
CONTACT_RECEIVER_EMAIL = required_env("CONTACT_RECEIVER_EMAIL")

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": required_env("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": required_env("CLOUDINARY_API_KEY"),
    "API_SECRET": required_env("CLOUDINARY_API_SECRET"),
}
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
