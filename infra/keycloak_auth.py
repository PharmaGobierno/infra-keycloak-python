from os import getenv

from keycloak import KeycloakOpenID


class KeycloakAuthService:
    def __init__(self, config: dict = {}):
        self.openid = KeycloakOpenID(
            server_url=config["KEYCLOAK_URL"] or getenv("KEYCLOAK_URL"),
            client_id=config["KEYCLOAK_CLIENT_ID"] or getenv("KEYCLOAK_CLIENT_ID", "admin-cli"),
            realm_name=config["KEYCLOAK_REALM"] or getenv("KEYCLOAK_REALM", "master"),
            client_secret_key=config["KEYCLOAK_CLIENT_SECRET"] or getenv("KEYCLOAK_CLIENT_SECRET"),
            verify=True,
        )

    def login(self, username, password):
        return self.openid.token(username, password)

    def refresh_token(self, refresh_token):
        return self.openid.refresh_token(refresh_token)

    def get_user_info(self, access_token):
        return self.openid.userinfo(access_token)

    def logout(self, refresh_token):
        return self.openid.logout(refresh_token)
