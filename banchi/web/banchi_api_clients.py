from banchi_client import Client, AuthenticatedClient
from banchi_client.api.v1 import refresh_token_v1_auth_refresh_get
from flask import session
import datetime
from werkzeug.exceptions import Unauthorized


class BanchiClient:
    def __init__(self):
        self.app = None

    def init_app(self, app):
        self.app = app

        self.base_url = app.config.get("BANCHI_API_BASE_URL")
        self.verify_ssl = app.config.get("BANCHI_API_VERIFY_SSL", False)

    def get_current_client(self, timeout=300, is_anonymous=False):
        tokens = session.get("tokens")
        expires_at = None
        if not tokens:
            if is_anonymous:
                return Client(
                    base_url=self.base_url, verify_ssl=self.verify_ssl, timeout=timeout
                )
            else:
                raise Unauthorized()

        expires_at = tokens.get("expires_at")
        if type(expires_at) == str:
            expires_at = datetime.datetime.fromisoformat(tokens.get("expires_at"))
        else:
            expires_at = datetime.datetime.fromisoformat(
                tokens.get("expires_at").strftime("%Y-%m-%dT%H:%M:%S")
            )

        now = datetime.datetime.now()

        if now + datetime.timedelta(minutes=2) > expires_at:
            refreash_token = tokens.get("refresh_token")
            client = AuthenticatedClient(
                base_url=self.base_url,
                token=refreash_token,
                verify_ssl=self.verify_ssl,
                timeout=timeout,
            )

            try:
                response = refresh_token_v1_auth_refresh_get.sync(
                    client=client,
                )
                tokens = response.to_dict()
            except Exception as e:
                print("Error refreshing token:", e)
                raise Unauthorized()

            session["tokens"].update(tokens)

        token = tokens.get("access_token")
        return AuthenticatedClient(
            base_url=self.base_url,
            token=token,
            verify_ssl=self.verify_ssl,
            timeout=timeout,
        )


def init_client(app):
    client.init_app(app)


client = BanchiClient()
