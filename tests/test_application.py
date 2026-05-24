import importlib.util
from pathlib import Path

import pytest

from student_task_manager.deployment import dev_admin_config, server_config, storage_secret
from student_task_manager.services.auth_service import DuplicateEmailError


def load_application_module():
    module_path = Path(__file__).resolve().parents[1] / "application.py"
    spec = importlib.util.spec_from_file_location("application_for_test", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_server_config_defaults_to_local_development() -> None:
    assert server_config({}) == ("127.0.0.1", 8081)


def test_server_config_uses_railway_port() -> None:
    assert server_config({"PORT": "12345"}) == ("0.0.0.0", 12345)


def test_server_config_allows_explicit_host_override() -> None:
    assert server_config({"HOST": "127.0.0.1", "PORT": "9000"}) == ("127.0.0.1", 9000)


def test_server_config_rejects_invalid_port() -> None:
    with pytest.raises(ValueError, match="PORT must be an integer"):
        server_config({"PORT": "not-a-port"})


def test_dev_admin_config_is_disabled_by_default() -> None:
    assert dev_admin_config({}) is None


def test_dev_admin_config_requires_password_when_enabled() -> None:
    with pytest.raises(RuntimeError, match="BIZZY_DEV_ADMIN_PASSWORD is required"):
        dev_admin_config({"BIZZY_CREATE_DEV_ADMIN": "1"})


def test_dev_admin_config_rejects_railway_environment() -> None:
    with pytest.raises(RuntimeError, match="dev-only"):
        dev_admin_config(
            {
                "BIZZY_CREATE_DEV_ADMIN": "1",
                "BIZZY_DEV_ADMIN_PASSWORD": "secret1234",
                "RAILWAY_ENVIRONMENT": "production",
            }
        )


def test_dev_admin_config_reads_explicit_credentials() -> None:
    assert dev_admin_config(
        {
            "BIZZY_CREATE_DEV_ADMIN": "true",
            "BIZZY_DEV_ADMIN_PASSWORD": "secret1234",
            "BIZZY_DEV_ADMIN_EMAIL": "dev@example.com",
            "BIZZY_DEV_ADMIN_NAME": "Dev Admin",
        }
    ) == ("dev@example.com", "Dev Admin", "secret1234")


def test_create_dev_admin_if_enabled_is_idempotent(monkeypatch, capsys) -> None:
    application = load_application_module()

    class FakeAuthService:
        def register(self, full_name, email, password, confirm_password):
            assert full_name == "Dev Admin"
            assert email == "dev@example.com"
            assert password == "secret1234"
            assert confirm_password == "secret1234"
            raise DuplicateEmailError("Unable to create account with those details")

    monkeypatch.setattr(application, "AuthService", FakeAuthService)

    created = application.create_dev_admin_if_enabled(
        {
            "BIZZY_CREATE_DEV_ADMIN": "1",
            "BIZZY_DEV_ADMIN_EMAIL": "dev@example.com",
            "BIZZY_DEV_ADMIN_NAME": "Dev Admin",
            "BIZZY_DEV_ADMIN_PASSWORD": "secret1234",
        }
    )

    assert created is False
    assert "Development admin already exists." in capsys.readouterr().out


def test_storage_secret_uses_local_fallback() -> None:
    assert storage_secret({}) == "dev-secret-key-do-not-use-in-production"


def test_storage_secret_rejects_missing_secret_for_deployed_run() -> None:
    with pytest.raises(RuntimeError, match="STORAGE_SECRET is required"):
        storage_secret({"PORT": "12345"})


def test_storage_secret_rejects_missing_secret_for_public_host() -> None:
    with pytest.raises(RuntimeError, match="STORAGE_SECRET is required"):
        storage_secret({"HOST": "0.0.0.0"})


def test_storage_secret_allows_localhost_host_fallback() -> None:
    assert storage_secret({"HOST": "localhost"}) == "dev-secret-key-do-not-use-in-production"


def test_storage_secret_uses_configured_secret() -> None:
    assert storage_secret({"STORAGE_SECRET": "configured-secret", "PORT": "12345"}) == (
        "configured-secret"
    )
