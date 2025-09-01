
from os import getenv
from typing import Optional

from keycloak import KeycloakOpenID
from keycloak.exceptions import (
    KeycloakAuthenticationError,
    KeycloakConnectionError as KeycloakLibConnectionError,
    KeycloakOperationError
)

from infra.exceptions import KeycloakTokenRefreshError, KeycloakConnectionError, KeycloakUnavailableError


class KeycloakAuthService:
    def __init__(self, config: Optional[dict] = None):
        config = config or {}

        self.openid = KeycloakOpenID(
            server_url=config.get("KEYCLOAK_URL") or getenv("KEYCLOAK_URL"),
            client_id=config.get("KEYCLOAK_CLIENT_ID")
            or getenv("KEYCLOAK_CLIENT_ID", "admin-cli"),
            realm_name=config.get("KEYCLOAK_REALM")
            or getenv("KEYCLOAK_REALM", "master"),
            client_secret_key=config.get("KEYCLOAK_CLIENT_SECRET")
            or getenv("KEYCLOAK_CLIENT_SECRET"),
            verify=config.get("KEYCLOAK_VERIFY_SSL", True),
        )

    def login(self, username, password):
        try:
            return self.openid.token(username, password)
        except KeycloakLibConnectionError as e:
            raise KeycloakUnavailableError(f"Keycloak server is not responding: {e}") from e
        except KeycloakAuthenticationError as e:
            raise KeycloakTokenRefreshError(f"Authentication failed: {e}") from e
        except KeycloakOperationError as e:
            raise KeycloakConnectionError(f"Keycloak operation failed: {e}") from e

    def refresh_token(self, refresh_token):
        try:
            return self.openid.refresh_token(refresh_token)
        except KeycloakLibConnectionError as e:
            raise KeycloakUnavailableError(f"Keycloak server is not responding during token refresh: {e}") from e
        except KeycloakOperationError as e:
            raise KeycloakConnectionError(f"Keycloak operation failed during token refresh: {e}") from e

    def get_user_info(self, access_token):
        try:
            return self.openid.userinfo(access_token)
        except KeycloakLibConnectionError as e:
            raise KeycloakUnavailableError(f"Keycloak server is not responding when getting user info: {e}") from e
        except KeycloakOperationError as e:
            raise KeycloakConnectionError(f"Keycloak operation failed when getting user info: {e}") from e

    def logout(self, refresh_token):
        try:
            return self.openid.logout(refresh_token)
        except KeycloakLibConnectionError as e:
            raise KeycloakUnavailableError(f"Keycloak server is not responding during logout: {e}") from e
        except KeycloakOperationError as e:
            raise KeycloakConnectionError(f"Keycloak operation failed during logout: {e}") from e
