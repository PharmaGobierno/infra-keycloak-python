# infra/exceptions.py


class KeycloakError(Exception):
    """Base exception for all Keycloak errors in the library."""

    pass


class KeycloakConnectionError(KeycloakError):
    """Errors related to connection issues with Keycloak server (timeout, network issues, server unavailable)."""

    pass


class KeycloakAdminError(KeycloakError):
    """Errors related to user or role management."""

    pass


class KeycloakAuthError(KeycloakError):
    """Errors related to authentication and tokens."""

    pass


class KeycloakUserCreationError(KeycloakAdminError):
    """Error creating a user in Keycloak."""

    pass


class KeycloakRoleAssignmentError(KeycloakAdminError):
    """Error assigning a role to a user."""

    pass


class KeycloakTokenRefreshError(KeycloakAuthError):
    """Error refreshing token."""

    pass


class KeycloakUnavailableError(KeycloakConnectionError):
    """Keycloak server is currently unavailable or not responding."""

    pass
