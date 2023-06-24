from rezource_client import Client, AuthenticatedClient
import datetime
from rezource_client.models import BodyAuthenticationApiV2UsersUsersLoginPost
from rezource_client.api.v2 import authentication_api_v2_users_users_login_post
import os
from loguru import logger


def get_client(settings, timeout=30):
    base_url = settings.REZOURCE_BASE_API_URL
    verify_ssl = settings.REZOURCE_API_VERIFY_SSL
    username = settings.REZOURCE_USERNAME
    password = settings.REZOURCE_PASSWORD

    tokens = login(username, password, base_url, verify_ssl, timeout)
    token = tokens.access_token
    return AuthenticatedClient(
        base_url=base_url, token=token, verify_ssl=verify_ssl, timeout=timeout
    )


def login(username, password, base_url, verify_ssl, timeout=30):
    client = Client(base_url=base_url, verify_ssl=verify_ssl, timeout=timeout)
    form_data = BodyAuthenticationApiV2UsersUsersLoginPost(
        username=username, password=password
    )
    tokens = authentication_api_v2_users_users_login_post.sync(
        client=client, form_data=form_data
    )

    return tokens
