import os
from collections.abc import Mapping


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
