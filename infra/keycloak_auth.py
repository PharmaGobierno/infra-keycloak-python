from os import getenv

from keycloak import KeycloakOpenID


class KeycloakAuthService:
    def __init__(self, config: dict = {}):
        self.openid = KeycloakOpenID(
            server_url=config["KEYCLOAK_URL"] or getenv("KEYCLOAK_URL"),
            client_id=config["CLIENT_ID"] or getenv("CLIENT_ID", "admin-cli"),
            realm_name=config["REALM_NAME"] or getenv("REALM_NAME", "master"),
            client_secret_key=config["CLIENT_SECRET"] or getenv("CLIENT_SECRET"),
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
