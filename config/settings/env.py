import os

from django.core.exceptions import ImproperlyConfigured


def required_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        raise ImproperlyConfigured(f"Missing required environment variable: {name}")
    return value


def env_bool(name: str) -> bool:
    value = required_env(name).strip().lower()
    truthy = {"1", "true", "yes", "on"}
    falsy = {"0", "false", "no", "off"}
    if value in truthy:
        return True
    if value in falsy:
        return False
    raise ImproperlyConfigured(f"Invalid boolean for {name}: {value}")


def env_int(name: str) -> int:
    raw = required_env(name)
    try:
        return int(raw)
    except ValueError as exc:
        raise ImproperlyConfigured(f"Invalid integer for {name}: {raw}") from exc


def env_float(name: str) -> float:
    raw = required_env(name)
    try:
        return float(raw)
    except ValueError as exc:
        raise ImproperlyConfigured(f"Invalid float for {name}: {raw}") from exc


def env_csv(name: str) -> list[str]:
    values = [item.strip() for item in required_env(name).split(",") if item.strip()]
    if not values:
        raise ImproperlyConfigured(f"Invalid CSV for {name}: no values provided")
    return values
