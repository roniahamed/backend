import os

settings_profile = os.getenv("DJANGO_ENV", "dev").lower()

if settings_profile == "prod":
    from .prod import *  # noqa: F403
elif settings_profile == "test":
    from .test import *  # noqa: F403
else:
    from .dev import *  # noqa: F403
