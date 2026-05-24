import os
from collections.abc import Mapping

DEV_ADMIN_FLAG = "BIZZY_CREATE_DEV_ADMIN"
DEV_ADMIN_PASSWORD = "BIZZY_DEV_ADMIN_PASSWORD"
DEV_ADMIN_EMAIL = "BIZZY_DEV_ADMIN_EMAIL"
DEV_ADMIN_NAME = "BIZZY_DEV_ADMIN_NAME"
STORAGE_SECRET = "STORAGE_SECRET"
LOCAL_HOSTS = {"127.0.0.1", "localhost", "::1", "[::1]"}


def server_config(env: Mapping[str, str] = os.environ) -> tuple[str, int]:
    """Return the host and port used by NiceGUI."""
    port_text = env.get("PORT", "8081")
    try:
        port = int(port_text)
    except ValueError as exc:
        raise ValueError("PORT must be an integer") from exc

    host = env.get("HOST")
    if not host:
        # Railway injects PORT and expects the app to listen publicly inside the
        # container; local runs stay on loopback unless HOST is set explicitly.
        host = "0.0.0.0" if "PORT" in env else "127.0.0.1"
    return host, port


def dev_admin_config(env: Mapping[str, str]) -> tuple[str, str, str] | None:
    enabled = env.get(DEV_ADMIN_FLAG, "").strip().lower()
    if enabled not in {"1", "true", "yes"}:
        return None

    if any(key.startswith("RAILWAY_") for key in env):
        raise RuntimeError(f"{DEV_ADMIN_FLAG} is dev-only and must not be enabled on Railway")

    password = env.get(DEV_ADMIN_PASSWORD, "")
    if not password:
        raise RuntimeError(f"{DEV_ADMIN_PASSWORD} is required when {DEV_ADMIN_FLAG} is enabled")

    email = env.get(DEV_ADMIN_EMAIL, "admin@example.com")
    full_name = env.get(DEV_ADMIN_NAME, "Admin User")
    return email, full_name, password


def _uses_public_host(env: Mapping[str, str]) -> bool:
    host = env.get("HOST", "").strip().lower()
    return bool(host and host not in LOCAL_HOSTS)


def storage_secret(env: Mapping[str, str] = os.environ) -> str:
    secret = env.get(STORAGE_SECRET)
    if secret:
        return secret
    if any(key.startswith("RAILWAY_") for key in env) or "PORT" in env or _uses_public_host(env):
        raise RuntimeError(f"{STORAGE_SECRET} is required for deployed runs")
    return "dev-secret-key-do-not-use-in-production"
