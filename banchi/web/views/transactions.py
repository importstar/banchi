from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
import datetime
import decimal
from collections import OrderedDict


from banchi_client import models
from banchi_client.api.v1 import (
    create_v1_account_books_post,
    create_v1_transactions_post,
    update_v1_account_books_account_book_id_put,
    update_v1_transactions_transaction_id_put,
    get_all_v1_account_books_get,
    get_all_v1_transactions_get,
    get_v1_account_books_account_book_id_get,
    get_v1_transactions_transaction_id_get,
    get_by_tags_v1_transactions_tags_tag_get,
    get_label_v1_account_books_account_book_id_label_get,
    delete_v1_account_books_account_book_id_delete,
    get_balance_v1_account_books_account_book_id_balance_get,
    delete_v1_transactions_transaction_id_delete,
)

from .. import banchi_api_clients
from .. import forms
from .. import utils

module = Blueprint("transactions", __name__, url_prefix="/transactions")


@module.route("")
@login_required
def index():

    return render_template(
        "/transactions/index.html",
    )


@module.route("/tags/<tag>")
@login_required
def show_by_tag(tag):

    client = banchi_api_clients.client.get_current_client()
    transactions = get_by_tags_v1_transactions_tags_tag_get.sync(client=client, tag=tag)

    account_id = ""
    if transactions.transactions:
        account_book_id = transactions.transactions[0].from_account_book.id
        account_book = get_v1_account_books_account_book_id_get.sync(
            client=client, account_book_id=account_book_id
        )
        account_id = account_book.account.id

    response = get_all_v1_account_books_get.sync(client=client, account_id=account_id)
    account_books = response.account_books

    display_names = utils.account_books.get_display_names(account_books)

    return render_template(
        "/transactions/show_by_tag.html",
        transactions=transactions,
        account_book_display_names=display_names,
        tag=tag,
    )


@module.route(
    "/add",
    methods=["GET", "POST"],
    defaults=dict(account_book_id=None, transaction_id=None),
)
@module.route("/<transaction_id>/edit", methods=["GET", "POST"])
@login_required
def add_or_edit(transaction_id):
    client = banchi_api_clients.client.get_current_client()
    account_book = None

    form = forms.transactions.TransactionForm()

    transaction = None
    if transaction_id:
        transaction = get_v1_transactions_transaction_id_get.sync(
            client=client, transaction_id=transaction_id
        )

        form = forms.transactions.TransactionForm(obj=transaction)

    display_names = utils.account_books.get_display_names(
        account_books, excluse_none_parent=True
    )
    account_book_choices = [
        (str(ab.id), display_names[ab.id])
        for ab in account_books
        if ab.id in display_names
    ]
    to_account_book_choices = account_book_choices

    account_book_choices = sorted(
        account_book_choices,
        key=lambda abn: abn[1],
    )

    # if not transaction:
    #     to_account_book_choices = [
    #         (str(ab.id), ab.display_name)
    #         for ab in response.account_books
    #         if ab != account_book
    #     ]

    #     to_account_book_choices = sorted(
    #         to_account_book_choices,
    #         key=lambda abn: abn[1],
    #     )

    form.to_account_book_id.choices = account_book_choices
    form.from_account_book_id.choices = account_book_choices

    # print(">>>", form.errors, form.data)
    if not form.validate_on_submit():
        if request.method == "GET" and account_book:
            form.from_account_book_id.data = str(account_book.id)
            form.to_account_book_id.data = str(account_book.id)

        if request.method == "GET" and transaction:
            form.to_account_book_id.data = str(transaction.to_account_book.id)
            form.from_account_book_id.data = str(transaction.from_account_book.id)
            form.value.data = decimal.Decimal(form.value.data)

        # if not transaction:
        #     form.from_account_book_id.render_kw = {"disabled": ""}

        return render_template(
            "/transactions/add-or-edit-transaction.html",
            account_book=account_book,
            form=form,
        )

    data = form.data.copy()
    data.pop("csrf_token")

    data["date"] = data["date"].isoformat()
    data["value"] = float(data["value"])

    if not transaction:
        transaction = models.CreatedTransaction.from_dict(data)
        response = create_v1_transactions_post.sync(client=client, body=transaction)
    else:
        transaction = models.UpdatedTransaction.from_dict(data)
        response = update_v1_transactions_transaction_id_put.sync(
            client=client, body=transaction, transaction_id=transaction_id
        )
    account_book = response.from_account_book

    return redirect(url_for("account_books.view", account_book_id=account_book.id))


@module.route("/<transaction_id>/delete")
@login_required
def delete(transaction_id):
    client = banchi_api_clients.client.get_current_client()
    transaction = delete_v1_transactions_transaction_id_delete.sync(
        client=client, transaction_id=transaction_id
    )

    account_book_id = transaction.from_account_book.id

    return redirect(url_for("account_books.view", account_book_id=account_book_id))
