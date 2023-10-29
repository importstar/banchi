from flask import Blueprint, render_template, redirect, url_for
import datetime


from banchi_client import models
from banchi_client.api.v1 import (
    create_space_v1_spaces_create_post,
    get_spaces_v1_spaces_get,
    get_space_v1_spaces_space_id_get,
    get_accounts_v1_accounts_get,
)

from .. import banchi_api_clients
from .. import forms

module = Blueprint("spaces", __name__, url_prefix="/spaces")


@module.route("")
def index():
    client = banchi_api_clients.client.get_current_client()
    response = get_spaces_v1_spaces_get.sync(client=client)

    return render_template("/spaces/index.html", spaces=response.spaces)


@module.route("/create", defaults=dict(space_id=None), methods=["GET", "POST"])
@module.route("/<space_id>/edit", methods=["GET", "POST"])
def create_or_edit(space_id):
    form = forms.spaces.SpaceForm()
    client = banchi_api_clients.client.get_current_client()
    space = None
    if space_id:
        space = get_space_v1_space_id_get.sync(client=client, id=space_id)
        form = forms.spaces.SpaceForm(obj=response.to_dict())

    if not form.validate_on_submit():
        return render_template("/spaces/create-or-edit.html", form=form)

    if not space:
        space = models.CreatedSpace.from_dict(form.data)
        response = create_space_v1_spaces_create_post.sync(
            client=client, json_body=space
        )
    else:
        space = models.UpdatedSpace.from_dict(form.data)
        response = update_space_v1_spaces_update_post.sync(
            client=client, json_body=space
        )

    if not response:
        print("error cannot save")

    return redirect(url_for("spaces.index"))


@module.route("/<space_id>")
def view(space_id):
    client = banchi_api_clients.client.get_current_client()
    space = get_space_v1_spaces_space_id_get.sync(client=client, space_id=space_id)
    response = get_accounts_v1_accounts_get.sync(client=client)

    return render_template("/spaces/view.html", space=space, accounts=response.accounts)
