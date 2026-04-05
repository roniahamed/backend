from .shared import *

SECRET_KEY = "test-secret-key-with-minimum-length-for-jwt-signing-12345"
DEBUG = False
ALLOWED_HOSTS = ["testserver", "localhost"]
CSRF_TRUSTED_ORIGINS = ["http://localhost"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test_db.sqlite3",
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "test-suite-cache",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
DEFAULT_FROM_EMAIL = "test@example.com"
CONTACT_RECEIVER_EMAIL = "receiver@example.com"

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": __import__("datetime").timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": __import__("datetime").timedelta(days=1),
}

CELERY_BROKER_URL = "memory://"
CELERY_RESULT_BACKEND = "cache+memory://"
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

UPLOAD_MAX_FILE_SIZE_BYTES = 2 * 1024 * 1024
UPLOAD_ALLOWED_IMAGE_MIME_TYPES = ("image/jpeg", "image/png", "image/webp")
