import datetime

from flask import (
    Blueprint,
    render_template,
    url_for,
    redirect,
    request,
    session,
    current_app,
    send_file,
    abort,
)
from flask_login import login_user, logout_user, login_required, current_user

from ... import forms

from ... import banchi_api_clients

from banchi_client import models
from banchi_client.api.v1 import (
    create_v1_users_create_post,
    get_all_v1_users_get,
    get_v1_users_user_id_get,
)


module = Blueprint("users", __name__, url_prefix="/users")


@module.route("")
def index():
    client = banchi_api_clients.client.get_current_client()
    response = get_all_v1_users_get.sync(client=client)
    return render_template("/admin/users/index.html", users=response.users)


@module.route("add", methods=["GET", "POST"], defaults=dict(user_id=None))
@module.route("edit", methods=["GET", "POST"])
def add_or_edit(user_id):
    form = forms.users.UserForm()

    client = banchi_api_clients.client.get_current_client()
    user = None
    if user_id:
        user = get_v1_users_user_id_get.sync(client=client, id=user_id)
        form = forms.users.UserForm(obj=user.to_dict())

    if not form.validate_on_submit():
        return render_template("/admin/users/add-or-edit.html", form=form)

    if not user:
        user = models.RegisteredUser.from_dict(form.data)
        response = create_v1_users_create_post.sync(client=client, json_body=user)
    else:
        user = models.UpdatedUser.from_dict(form.data)
        response = update_v1_users_update_post.sync(client=client, json_body=user)

    if not response:
        print("error cannot save")

    return redirect(url_for("admin.users.index"))
