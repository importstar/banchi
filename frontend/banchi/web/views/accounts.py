from flask import Blueprint, render_template, redirect, url_for
import datetime


from banchi_client import models
from banchi_client.api.v1 import (
    create_account_v1_accounts_create_post,
    get_accounts_v1_accounts_get,
    get_account_v1_accounts_account_id_get,
)

from .. import banchi_api_clients
from .. import forms

module = Blueprint("accounts", __name__, url_prefix="/accounts")


@module.route("")
def index():
    client = banchi_api_clients.client.get_current_client()
    response = get_accounts_v1_accounts_get.sync(client=client)

    return render_template("/accounts/index.html", accounts=response.accounts)


@module.route("/create", defaults=dict(account_id=None), methods=["GET", "POST"])
@module.route("/<account_id>/edit", methods=["GET", "POST"])
def create_or_edit(account_id):
    form = forms.accounts.SpaceForm()
    client = banchi_api_clients.client.get_current_client()
    account = None
    if account_id:
        account = get_account_v1_account_id_get.sync(client=client, id=account_id)
        form = forms.accounts.SpaceForm(obj=response.to_dict())

    if not form.validate_on_submit():
        return render_template("/accounts/create-or-edit.html", form=form)

    if not account:
        account = models.CreatedSpace.from_dict(form.data)
        response = create_account_v1_accounts_create_post.sync(
            client=client, json_body=account
        )
    else:
        account = models.UpdatedSpace.from_dict(form.data)
        response = update_account_v1_accounts_update_post.sync(
            client=client, json_body=account
        )

    if not response:
        print("error cannot save")

    return redirect(url_for("accounts.index"))


@module.route("/<account_id>")
def view(account_id):
    client = banchi_api_clients.client.get_current_client()
    account = get_account_v1_accounts_account_id_get.sync(
        client=client, account_id=account_id
    )

    return render_template("/accounts/view.html", account=account)
