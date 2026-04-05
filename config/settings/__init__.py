import os

from django.core.exceptions import ImproperlyConfigured

settings_profile = os.getenv("DJANGO_ENV")
settings_module_target = os.getenv("DJANGO_SETTINGS_MODULE", "")

if settings_profile is None or settings_profile.strip() == "":
    # why: Direct imports like config.settings.test are valid for tests and tooling.
    if settings_module_target in {
        "config.settings.test",
        "config.settings.dev",
        "config.settings.prod",
    }:
        settings_profile = ""
    else:
        raise ImproperlyConfigured("Missing required environment variable: DJANGO_ENV")

if settings_profile:
    settings_profile = settings_profile.lower()

    if settings_profile == "prod":
        from .prod import *  # noqa: F403
    elif settings_profile == "test":
        from .test import *  # noqa: F403
    elif settings_profile == "dev":
        from .dev import *  # noqa: F403
    else:
        raise ImproperlyConfigured(f"Unsupported DJANGO_ENV value: {settings_profile}")
