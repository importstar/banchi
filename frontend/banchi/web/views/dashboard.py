import datetime
from flask import Blueprint, render_template
from flask_login import login_required, current_user

import mongoengine as me
from .. import models
from .. import acl


module = Blueprint("dashboard", __name__, url_prefix="/dashboard")


def index_admin():
    now = datetime.datetime.now()

    return render_template(
        "/dashboard/index-admin.html",
        now=datetime.datetime.now(),
    )


def index_user():
    now = datetime.datetime.now()
    return render_template(
        "/dashboard/index-user.html",
    )


@module.route("/")
@login_required
def index():
    user = current_user._get_current_object()
    if user.has_roles("admin"):
        return index_admin()

    return index_user()


@module.route("/me")
@login_required
def me():
    return index_user()
