import datetime
from flask import Blueprint, render_template
from flask_login import login_required, current_user

from .. import models
from .. import acl


module = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@module.route("/admin")
@acl.roles_required("admin")
def index_admin():
    now = datetime.datetime.now()

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
