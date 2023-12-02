from flask import Blueprint, render_template, request, redirect, url_for
import datetime
from collections import OrderedDict


from banchi_client import models
from banchi_client.api.v1 import (
    create_v1_accounts_create_post,
    get_all_v1_accounts_get,
    get_all_v1_account_books_get,
    get_balance_v1_account_books_account_book_id_balance_get,
    get_v1_accounts_account_id_get,
)

from .. import banchi_api_clients
from .. import forms

module = Blueprint("accounts", __name__, url_prefix="/accounts")


@module.route("")
def index():
    client = banchi_api_clients.client.get_current_client()
    response = get_all_v1_accounts_get.sync(client=client)

    return render_template("/accounts/index.html", accounts=response.accounts)


@module.route("/create", defaults=dict(account_id=None), methods=["GET", "POST"])
@module.route("/<account_id>/edit", methods=["GET", "POST"])
def create_or_edit(account_id):
    form = forms.accounts.AccountForm()
    client = banchi_api_clients.client.get_current_client()
    account = None
    if account_id:
        account = get_account_v1_account_id_get.sync(client=client, id=account_id)
        form = forms.accounts.AccountForm(obj=response.to_dict())

    if not form.validate_on_submit():
        return render_template("/accounts/create-or-edit.html", form=form)

    data = form.data.copy()
    data["space_id"] = request.args.get("space_id")

    if not account:
        account = models.CreatedAccount.from_dict(data)
        response = create_v1_accounts_create_post.sync(client=client, json_body=account)
    else:
        account = models.UpdatedAccount.from_dict(data)
        response = update_v1_accounts_update_post.sync(client=client, json_body=account)

    if not response:
        print("error cannot save")

    return redirect(url_for("accounts.index"))


@module.route("/<account_id>")
def view(account_id):
    client = banchi_api_clients.client.get_current_client()
    account = get_v1_accounts_account_id_get.sync(client=client, account_id=account_id)
    response = get_all_v1_account_books_get.sync(client=client, account_id=account_id)

    account_books = response.account_books
    balances = dict()
    display_account_books = dict()

    for account_book in account_books:
        display_account_books[account_book.id] = dict(
            name=get_account_book_display_name(account_book),
            account_balance=get_balance_v1_account_books_account_book_id_balance_get.sync(
                client=client, account_book_id=account_book.id
            ),
            obj=account_book,
        )

    display_account_books = OrderedDict(
        sorted(display_account_books.items(), key=lambda a: a[1]["name"])
    )

    return render_template(
        "/accounts/view.html",
        account=account,
        account_books=account_books,
        balances=balances,
        display_account_books=display_account_books,
    )


def get_account_book_display_name(account_book):
    if hasattr(account_book, "parent") and account_book.parent:
        return f"{get_account_book_display_name(account_book.parent)} >> {account_book.name}"

    return account_book.name
