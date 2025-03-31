from os import getenv
from typing import Any, Dict, List, cast

from keycloak import KeycloakAdmin


class KeycloakAdminService:
    def __init__(self, config: dict = None):

        config = config or {}

        self.admin = KeycloakAdmin(
            server_url=config.get("KEYCLOAK_URL") or getenv("KEYCLOAK_URL"),
            username=config.get("KEYCLOAK_ADMIN_USERNAME") or getenv("KEYCLOAK_ADMIN_USERNAME"),
            password=config.get("KEYCLOAK_ADMIN_PASSWORD") or getenv("KEYCLOAK_ADMIN_PASSWORD"),
            realm_name=config.get("KEYCLOAK_REALM") or getenv("KEYCLOAK_REALM", "master"),
            user_realm_name=config.get("KEYCLOAK_ADMIN_REALM") or getenv("KEYCLOAK_ADMIN_REALM"),
            client_id=config.get("KEYCLOAK_CLIENT_ID") or getenv("KEYCLOAK_CLIENT_ID", "admin-cli"),
            verify=True,
        )

    def create_user(self, user_data):
        return self.admin.create_user(user_data)

    def assign_role(self, user_id, role_name):
        roles = cast(List[Dict[str, Any]], self.admin.get_realm_roles())
        role = next((r for r in roles if r["name"] == role_name), None)

        if not role:
            raise ValueError(f"Role '{role_name}' not found in realm.")

        self.admin.assign_realm_roles(user_id=user_id, roles=[role])
