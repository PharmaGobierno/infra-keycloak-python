from os import getenv
from typing import Optional

from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakAuthenticationError

from infra.exceptions import KeycloakTokenRefreshError


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
        except KeycloakAuthenticationError as e:
            raise KeycloakTokenRefreshError(f"Authentication failed: {e}") from e

    def refresh_token(self, refresh_token):
        return self.openid.refresh_token(refresh_token)

    def get_user_info(self, access_token):
        return self.openid.userinfo(access_token)

    def logout(self, refresh_token):
        return self.openid.logout(refresh_token)
