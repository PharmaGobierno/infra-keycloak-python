from unittest.mock import MagicMock

import pytest

from infra.keycloak_auth import KeycloakAuthService


@pytest.fixture
def mock_config():
    return {
        "KEYCLOAK_URL": "http://localhost:8080/",
        "REALM_NAME": "myrealm",
        "CLIENT_ID": "my-client",
        "CLIENT_SECRET": "my-secret",
    }


def test_login(monkeypatch, mock_config):
    mock_openid = MagicMock()
    monkeypatch.setattr(
        "infra.keycloak_auth.KeycloakOpenID", lambda **kwargs: mock_openid
    )

    service = KeycloakAuthService(mock_config)
    service.login("user", "pass")

    mock_openid.token.assert_called_once_with("user", "pass")


def test_refresh_token(monkeypatch, mock_config):
    mock_openid = MagicMock()
    monkeypatch.setattr(
        "infra.keycloak_auth.KeycloakOpenID", lambda **kwargs: mock_openid
    )

    service = KeycloakAuthService(mock_config)
    service.refresh_token("ref-token")

    mock_openid.refresh_token.assert_called_once_with("ref-token")
