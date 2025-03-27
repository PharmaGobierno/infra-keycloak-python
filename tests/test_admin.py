from unittest.mock import MagicMock

import pytest

from infra.keycloak_admin import KeycloakAdminService


@pytest.fixture
def mock_config():
    return {
        "KEYCLOAK_URL": "http://localhost:8080/",
        "ADMIN_USERNAME": "admin",
        "ADMIN_PASSWORD": "admin",
        "REALM_NAME": "myrealm",
        "ADMIN_REALM": "master",
        "CLIENT_ID": "admin-cli",
    }


def test_create_user(monkeypatch, mock_config):
    mock_admin_instance = MagicMock()
    monkeypatch.setattr(
        "infra.keycloak_admin.KeycloakAdmin", lambda **kwargs: mock_admin_instance
    )

    service = KeycloakAdminService(mock_config)

    user_data = {"username": "testuser"}
    service.create_user(user_data)

    mock_admin_instance.create_user.assert_called_once_with(user_data)


def test_assign_role(monkeypatch, mock_config):
    mock_admin_instance = MagicMock()
    mock_admin_instance.get_realm_roles.return_value = [
        {"name": "user", "id": "role-id"}
    ]
    monkeypatch.setattr(
        "infra.keycloak_admin.KeycloakAdmin", lambda **kwargs: mock_admin_instance
    )

    service = KeycloakAdminService(mock_config)
    service.assign_role("user-id", "user")

    mock_admin_instance.assign_realm_roles.assert_called_once()
