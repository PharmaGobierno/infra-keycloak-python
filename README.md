# KeycloakLib

Una librería en Python para interactuar con Keycloak, separando responsabilidades entre autenticación y administración de usuarios.

## Estructura

- `keycloak_auth.py`: Maneja login, logout, refresh y obtención de información del usuario.
- `keycloak_admin.py`: Permite crear usuarios, asignar roles y otras tareas administrativas.
- `keycloak_service.py`: Clase que une ambas interfaces.

## Requisitos

- Python 3.8+
- `python-keycloak`

```bash
pip install python-keycloak
```

## Uso básico

```python
from keycloak_lib.keycloak_auth import KeycloakAuthService
from keycloak_lib.keycloak_admin import KeycloakAdminService


admin = KeycloakAdminService(CONFIG)
auth = KeycloakAuthService(CONFIG)


# Crear un usuario
admin.create_user({...})

# Login
tokens = auth.login("user", "pass")
```
