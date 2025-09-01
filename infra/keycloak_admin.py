from os import getenv
from typing import Any, Dict, List, Optional, cast

from keycloak import KeycloakAdmin
from keycloak.exceptions import (
   KeycloakOperationError,
   KeycloakConnectionError as KeycloakLibConnectionError,
)

from infra.exceptions import KeycloakRoleAssignmentError, KeycloakUserCreationError, KeycloakConnectionError, KeycloakUnavailableError


class KeycloakAdminService:
    def __init__(self, config: Optional[dict] = None):
        config = config or {}

        self.admin = KeycloakAdmin(
            server_url=config.get("KEYCLOAK_URL") or getenv("KEYCLOAK_URL"),
            username=config.get("KEYCLOAK_ADMIN_USERNAME")
            or getenv("KEYCLOAK_ADMIN_USERNAME"),
            password=config.get("KEYCLOAK_ADMIN_PASSWORD")
            or getenv("KEYCLOAK_ADMIN_PASSWORD"),
            realm_name=config.get("KEYCLOAK_REALM")
            or getenv("KEYCLOAK_REALM", "master"),
            user_realm_name=config.get("KEYCLOAK_ADMIN_REALM")
            or getenv("KEYCLOAK_ADMIN_REALM"),
            client_id=config.get("KEYCLOAK_CLIENT_ID")
            or getenv("KEYCLOAK_CLIENT_ID", "admin-cli"),
            verify=config.get("KEYCLOAK_VERIFY_SSL", True),
        )

    def create_user(self, user_data: Dict[str, Any]) -> str:
        try:
            return self.admin.create_user(user_data)
        except KeycloakLibConnectionError as e:
            raise KeycloakUnavailableError(f"Keycloak server is not responding when creating user: {e}") from e
        except KeycloakOperationError as e:
            raise KeycloakUserCreationError(f"Error creating user: {e}") from e

    def assign_role(self, user_id: str, role_name: str) -> None:
        try:
            roles = cast(List[Dict[str, Any]], self.admin.get_realm_roles())
            role = next((r for r in roles if r["name"] == role_name), None)

            if not role:
                raise ValueError(f"Role '{role_name}' not found in realm.")

            self.admin.assign_realm_roles(user_id=user_id, roles=[role])
        except KeycloakLibConnectionError as e:
            raise KeycloakUnavailableError(f"Keycloak server is not responding when assigning role: {e}") from e
        except KeycloakOperationError as e:
            raise KeycloakRoleAssignmentError(f"Error assigning role: {e}") from e
