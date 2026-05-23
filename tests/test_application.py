import pytest

from student_task_manager.deployment import server_config


def test_server_config_defaults_to_local_development() -> None:
    assert server_config({}) == ("127.0.0.1", 8081)


def test_server_config_uses_railway_port() -> None:
    assert server_config({"PORT": "12345"}) == ("0.0.0.0", 12345)


def test_server_config_allows_explicit_host_override() -> None:
    assert server_config({"HOST": "127.0.0.1", "PORT": "9000"}) == ("127.0.0.1", 9000)


def test_server_config_rejects_invalid_port() -> None:
    with pytest.raises(ValueError, match="PORT must be an integer"):
        server_config({"PORT": "not-a-port"})
