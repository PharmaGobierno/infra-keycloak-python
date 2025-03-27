from os import getenv
from typing import Any, Dict, List, cast

from keycloak import KeycloakAdmin


class KeycloakAdminService:
    def __init__(self, config: dict = {}):

        self.admin = KeycloakAdmin(
            server_url=config["KEYCLOAK_URL"] or getenv("KEYCLOAK_URL"),
            username=config["ADMIN_USERNAME"] or getenv("ADMIN_USERNAME"),
            password=config["ADMIN_PASSWORD"] or getenv("ADMIN_PASSWORD"),
            realm_name=config["REALM_NAME"] or getenv("REALM_NAME", "master"),
            user_realm_name=config["ADMIN_REALM"] or getenv("ADMIN_REALM"),
            client_id=config.get("CLIENT_ID") or getenv("CLIENT_ID", "admin-cli"),
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
