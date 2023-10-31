from flask import Blueprint, render_template, request, redirect, url_for
import datetime


from banchi_client import models
from banchi_client.api.v1 import (
    create_v1_account_books_create_post,
    get_all_v1_account_books_get,
    get_v1_account_books_account_book_id_get,
)

from .. import banchi_api_clients
from .. import forms

module = Blueprint("account_books", __name__, url_prefix="/account-books")


@module.route("")
def index():
    client = banchi_api_clients.client.get_current_client()
    response = get_all_v1_account_books_get.sync(client=client)

    return render_template(
        "/account_books/index.html", account_books=response.account_books
    )


@module.route("/create", defaults=dict(account_book_id=None), methods=["GET", "POST"])
@module.route("/<account_book_id>/edit", methods=["GET", "POST"])
def create_or_edit(account_book_id):
    form = forms.account_books.AccountBookForm()
    client = banchi_api_clients.client.get_current_client()
    account_book = None
    account_id = request.args.get("account_id")

    if account_book_id:
        account_book = get_v1_account_books_account_book_id_get.sync(
            client=client, id=account_book_id
        )
        form = forms.account_books.AccountBookForm(obj=response.to_dict())

    if account_id or account_book_id:
        if account_book_id:
            account_id = account_book.account.id

        response = get_all_v1_account_books_get.sync(
            client=client, account_id=account_id
        )

        form.parent_id.choices.extend(
            [
                (account_book.to_dict()["id"], account_book.name)
                for account_book in response.account_books
            ]
        )

    if not form.validate_on_submit():
        return render_template("/account_books/create-or-edit.html", form=form)

    data = form.data.copy()
    print("data", data)
    if data["parent_id"] == "-":
        data["parent_id"] = None
    if account_id:
        data["account_id"] = account_id
    else:
        data["account_id"] = None

    if not account_book:
        account_book = models.CreatedAccountBook.from_dict(data)
        response = create_v1_account_books_create_put.sync(
            client=client, json_body=account_book
        )
    else:
        account_book = models.UpdatedAccountBook.from_dict(data)
        response = update_v1_account_books_update_post.sync(
            client=client, json_body=account_book
        )

    if not response:
        print("error cannot save")

    return redirect(url_for("account_books.index"))


@module.route("/<account_book_id>")
def view(account_book_id):
    client = banchi_api_clients.client.get_current_client()
    account_book = get_v1_account_books_account_book_id_get.sync(
        client=client, account_book_id=account_book_id
    )

    return render_template("/account_books/view.html", account_book=account_book)
