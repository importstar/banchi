import datetime
from flask import Blueprint, render_template
from flask_login import login_required, current_user

from .. import acl

from .. import banchi_api_clients

from banchi_client import models


from banchi_client.api.v1 import (
    get_all_v1_spaces_get,
)


module = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@module.route("/admin")
@acl.roles_required("admin")
def index_admin():
    now = datetime.datetime.now()

    client = banchi_api_clients.client.get_current_client()
    response = get_all_v1_spaces_get.sync(client=client)
    print("response->", response)

    return render_template(
        "/dashboard/index-admin.html",
        now=datetime.datetime.now(),
    )


@module.route("")
@login_required
def index():
    user = current_user._get_current_object()
    return render_template(
        "/dashboard/index-user.html",
    )


@module.route("/me")
@login_required
def me():
    return index_user()
