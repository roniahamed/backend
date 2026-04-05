from datetime import timedelta

import environ
import sentry_sdk
from celery.schedules import crontab
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from .env import env_bool, env_csv, env_float, env_int, required_env
from .shared import *

env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = required_env("DJANGO_SECRET_KEY")
DEBUG = env_bool("DJANGO_DEBUG")
ALLOWED_HOSTS = env_csv("DJANGO_ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = env_csv("DJANGO_CSRF_TRUSTED_ORIGINS")
CORS_ALLOWED_ORIGINS = env_csv("CORS_ALLOWED_ORIGINS")

DATABASES = {"default": env.db("DATABASE_URL")}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": required_env("REDIS_CACHE_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_CONNECT_TIMEOUT": env_int("REDIS_SOCKET_CONNECT_TIMEOUT_SECONDS"),
            "SOCKET_TIMEOUT": env_int("REDIS_SOCKET_TIMEOUT_SECONDS"),
        },
        "TIMEOUT": env_int("REDIS_CACHE_DEFAULT_TIMEOUT_SECONDS"),
    }
}

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = env_int("DJANGO_SECURE_HSTS_SECONDS")
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS")
SECURE_HSTS_PRELOAD = env_bool("DJANGO_SECURE_HSTS_PRELOAD")
SESSION_COOKIE_SECURE = env_bool("DJANGO_SESSION_COOKIE_SECURE")
CSRF_COOKIE_SECURE = env_bool("DJANGO_CSRF_COOKIE_SECURE")
SECURE_SSL_REDIRECT = env_bool("DJANGO_SECURE_SSL_REDIRECT")

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=env_int("JWT_ACCESS_MINUTES")),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=env_int("JWT_REFRESH_DAYS")),
    "ROTATE_REFRESH_TOKENS": env_bool("JWT_ROTATE_REFRESH_TOKENS"),
    "BLACKLIST_AFTER_ROTATION": env_bool("JWT_BLACKLIST_AFTER_ROTATION"),
    "ALGORITHM": required_env("JWT_ALGORITHM"),
    "SIGNING_KEY": required_env("JWT_SIGNING_KEY"),
    "AUTH_HEADER_TYPES": (required_env("JWT_AUTH_HEADER_TYPE"),),
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = required_env("EMAIL_HOST")
EMAIL_PORT = env_int("EMAIL_PORT")
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS")
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

CELERY_BROKER_URL = required_env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = required_env("CELERY_RESULT_BACKEND")
CELERY_TASK_ALWAYS_EAGER = env_bool("CELERY_TASK_ALWAYS_EAGER")
CELERY_TASK_EAGER_PROPAGATES = env_bool("CELERY_TASK_EAGER_PROPAGATES")
CELERY_WORKER_CONCURRENCY = env_int("CELERY_WORKER_CONCURRENCY")
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = env_bool("CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP")

UPLOAD_MAX_FILE_SIZE_BYTES = env_int("UPLOAD_MAX_FILE_SIZE_BYTES")
UPLOAD_ALLOWED_IMAGE_MIME_TYPES = tuple(env_csv("UPLOAD_ALLOWED_IMAGE_MIME_TYPES"))

SENTRY_DSN = required_env("SENTRY_DSN")
SENTRY_TRACES_SAMPLE_RATE = env_float("SENTRY_TRACES_SAMPLE_RATE")
SENTRY_PROFILES_SAMPLE_RATE = env_float("SENTRY_PROFILES_SAMPLE_RATE")

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[DjangoIntegration(), CeleryIntegration(), RedisIntegration()],
    send_default_pii=False,
    traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE,
    profiles_sample_rate=SENTRY_PROFILES_SAMPLE_RATE,
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "format": "{\"time\":\"%(asctime)s\",\"level\":\"%(levelname)s\",\"logger\":\"%(name)s\",\"message\":\"%(message)s\"}"
        },
        "plain": {"format": "%(levelname)s %(name)s %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "plain",
        },
        "json_console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
    },
    "root": {
        "handlers": ["console", "json_console"],
        "level": "INFO",
    },
}

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_BEAT_SCHEDULE = {
    "warm-blog-cache": {
        "task": "apps.blog.tasks.warm_blog_cache_task",
        "schedule": crontab(minute="*/5"),
    },
    "aggregate-tag-usage": {
        "task": "apps.blog.tasks.aggregate_tag_usage_task",
        "schedule": crontab(minute="*/10"),
    },
}

