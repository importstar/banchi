from flask import Blueprint, render_template, redirect, url_for, request
import datetime


from banchi_client import models
from banchi_client.api.v1 import (
    add_v1_spaces_space_id_roles_post,
    create_v1_spaces_post,
    get_all_v1_spaces_get,
    get_v1_spaces_space_id_get,
    get_all_v1_accounts_get,
    get_all_v1_spaces_space_id_roles_get,
    get_v1_spaces_space_id_roles_space_role_id_get,
    get_all_v1_users_get,
    get_accounts_v1_spaces_space_id_accounts_get,
    update_v1_spaces_space_id_put,
    update_v1_spaces_space_id_roles_space_role_id_put,
)

from .. import banchi_api_clients
from .. import forms

module = Blueprint("spaces", __name__, url_prefix="/spaces")


@module.route("")
def index():
    client = banchi_api_clients.client.get_current_client()
    response = get_all_v1_spaces_get.sync(client=client)

    return render_template("/spaces/index.html", spaces=response.spaces)


@module.route("/create", defaults=dict(space_id=None), methods=["GET", "POST"])
@module.route("/<space_id>/edit", methods=["GET", "POST"])
def create_or_edit(space_id):
    form = forms.spaces.SpaceForm()
    client = banchi_api_clients.client.get_current_client()
    space = None
    if space_id:
        space = get_v1_spaces_space_id_get.sync(client=client, space_id=space_id)
        form = forms.spaces.SpaceForm(obj=space)

    if not form.validate_on_submit():
        return render_template("/spaces/create-or-edit.html", form=form)

    if not space:
        space = models.CreatedSpace.from_dict(form.data)
        response = create_v1_spaces_post.sync(client=client, json_body=space)
    else:
        space = models.UpdatedSpace.from_dict(form.data)
        response = update_v1_spaces_space_id_put.sync(
            client=client, json_body=space, space_id=space_id
        )

    if not response:
        print("error cannot save")

    return redirect(url_for("spaces.index"))


@module.route("/<space_id>")
def view(space_id):
    client = banchi_api_clients.client.get_current_client()
    space = get_v1_spaces_space_id_get.sync(client=client, space_id=space_id)
    account = get_accounts_v1_spaces_space_id_accounts_get.sync(
        client=client, space_id=space_id
    )

    return render_template("/spaces/view.html", space=space, account=account)


@module.route("/<space_id>/roles")
def list_roles(space_id):
    client = banchi_api_clients.client.get_current_client()
    space_role_response = get_all_v1_spaces_space_id_roles_get.sync(
        client=client, space_id=space_id
    )
    space = get_v1_spaces_space_id_get.sync(client=client, space_id=space_id)

    return render_template(
        "/spaces/list-roles.html",
        space_roles=space_role_response.space_roles,
        space=space,
    )


@module.route(
    "/<space_id>/roles/add", methods=["GET", "POST"], defaults=dict(space_role_id=None)
)
@module.route("/<space_id>/roles/<space_role_id>/edit", methods=["GET", "POST"])
def add_or_edit_role(space_id, space_role_id):
    client = banchi_api_clients.client.get_current_client()

    user_response = get_all_v1_users_get.sync(client=client)
    space = get_v1_spaces_space_id_get.sync(client=client, space_id=space_id)

    form = forms.spaces.SpaceRoleForm()

    space_role = None
    if space_role_id:
        space_role = get_v1_spaces_space_id_roles_space_role_id_get.sync(
            client=client, space_id=space_id, space_role_id=space_role_id
        )

    if request.method == "GET" and space_role:
        form = forms.spaces.SpaceRoleForm(obj=space_role)
        form.member_id.data = space_role.member.id

    form.member_id.choices = [
        (str(user.id), f"{ user.first_name } { user.last_name }")
        for user in user_response.users
    ]

    if not form.validate_on_submit():
        return render_template("/spaces/add-or-edit-role.html", form=form, space=space)

    if not space_role:
        space_role = models.CreatedSpaceRole.from_dict(form.data)
        response = add_v1_spaces_space_id_roles_post.sync(
            client=client, json_body=space_role, space_id=space_id
        )
    else:
        space_role = models.UpdatedSpaceRole.from_dict(form.data)
        response = update_v1_spaces_space_id_roles_space_role_id_put.sync(
            client=client,
            json_body=space_role,
            space_id=space_id,
            space_role_id=space_role_id,
        )

    if not response:
        print("error cannot save")

    return redirect(url_for("spaces.list_roles", space_id=space_id))
