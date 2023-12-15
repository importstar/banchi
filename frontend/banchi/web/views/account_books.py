from flask import Blueprint, render_template, request, redirect, url_for
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
    get_label_v1_account_books_account_book_id_label_get,
    get_balance_v1_account_books_account_book_id_balance_get,
)

from .. import banchi_api_clients
from .. import forms
from .. import utils

module = Blueprint("account_books", __name__, url_prefix="/account-books")


@module.route("")
def index():
    account_id = request.args.get("account_id")
    account_books = []

    if not account_id:
        return redirect("dashboard.index")

    client = banchi_api_clients.client.get_current_client()
    response = get_all_v1_account_books_get.sync(client=client, account_id=account_id)

    account_books = response.account_books
    balances = dict()
    display_account_books = dict()

    display_names = utils.account_books.get_display_names(account_books)
    for account_book in account_books:
        display_account_books[account_book.id] = dict(
            name=display_names[account_book.id],
            account_balance=get_balance_v1_account_books_account_book_id_balance_get.sync(
                client=client, account_book_id=account_book.id
            ),
            obj=account_book,
        )

    display_account_books = OrderedDict(
        sorted(display_account_books.items(), key=lambda a: a[1]["name"])
    )

    return render_template(
        "/account_books/index.html",
        account_books=account_books,
        balances=balances,
        display_account_books=display_account_books,
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
        account_id = account_book.account.id

    if account_id:
        response = get_all_v1_account_books_get.sync(
            client=client, account_id=account_id
        )

        account_books = response.account_books

        display_names = utils.account_books.get_display_names(account_books)

        form.parent_id.choices.extend(
            sorted(
                [
                    (account_book.id, display_names[account_book.id])
                    for account_book in account_books
                ],
                key=lambda abn: abn[1],
            )
        )

    if not form.validate_on_submit():
        return render_template("/account_books/create-or-edit.html", form=form)

    data = form.data.copy()
    if data["parent_id"] == "-":
        data["parent_id"] = None
    if account_id:
        data["account_id"] = account_id
    else:
        data["account_id"] = None

    if not account_book:
        account_book = models.CreatedAccountBook.from_dict(data)
        response = create_v1_account_books_post.sync(
            client=client, json_body=account_book
        )
    else:
        account_book = models.UpdatedAccountBook.from_dict(data)
        response = update_v1_account_books_account_book_id_put.sync(
            client=client, json_body=account_book
        )

    if not response:
        print("error cannot save")

    return redirect(url_for("accounts.view", account_id=account_id))


@module.route("/<account_book_id>")
def view(account_book_id):
    client = banchi_api_clients.client.get_current_client()
    account_book = get_v1_account_books_account_book_id_get.sync(
        client=client, account_book_id=account_book_id
    )

    response = get_all_v1_transactions_get.sync(
        client=client,
        from_account_book_id=account_book.id,
        to_account_book_id=account_book.id,
    )
    transactions = response.transactions

    label = get_label_v1_account_books_account_book_id_label_get.sync(
        client=client, account_book_id=account_book.id
    )
    balance = get_balance_v1_account_books_account_book_id_balance_get.sync(
        client=client, account_book_id=account_book.id
    )

    response = get_all_v1_account_books_get.sync(
        client=client, account_id=account_book.account.id
    )
    account_books = response.account_books

    display_names = utils.account_books.get_display_names(account_books)

    account_book_children = [
        ab for ab in account_books if ab.parent and ab.parent.id == account_book.id
    ]

    def get_balance_sub_balance(account_book, balance):
        for b in balance:
            if b.id == account_book.id:
                return b
        return None

    return render_template(
        "/account_books/view.html",
        account_book=account_book,
        account_book_display_names=display_names,
        transactions=transactions,
        label=label,
        balance=balance,
        account_book_children=account_book_children,
        get_balance_sub_balance=get_balance_sub_balance,
    )


@module.route(
    "/<account_book_id>/transactions/add",
    methods=["GET", "POST"],
    defaults=dict(transaction_id=None),
)
@module.route(
    "/<account_book_id>/transactions/<transaction_id>/edit", methods=["GET", "POST"]
)
def add_or_edit_transaction(account_book_id, transaction_id):
    client = banchi_api_clients.client.get_current_client()
    account_book = get_v1_account_books_account_book_id_get.sync(
        client=client, account_book_id=account_book_id
    )

    if not account_book:
        return redirect("sites.index")

    response = get_all_v1_account_books_get.sync(
        client=client, account_id=account_book.account.id
    )

    account_books = response.account_books

    form = forms.transactions.TransactionForm()

    transaction = None
    if transaction_id:
        transaction = get_v1_transactions_transaction_id_get.sync(
            client=client, transaction_id=transaction_id
        )

        form = forms.transactions.TransactionForm(obj=transaction)

    display_names = utils.account_books.get_display_names(account_books)
    account_book_choices = [(str(ab.id), display_names[ab.id]) for ab in account_books]
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

    if not form.validate_on_submit():
        if request.method == "GET":
            form.from_account_book_id.data = str(account_book.id)
            form.to_account_book_id.data = str(account_book.id)

        if request.method == "GET" and transaction:
            form.to_account_book_id.data = str(transaction.to_account_book.id)
            form.from_account_book_id.data = str(transaction.from_account_book.id)
            form.value.data = decimal.Decimal(form.value.data)

        # if not transaction:
        #     form.from_account_book_id.render_kw = {"disabled": ""}

        return render_template(
            "/account_books/add-or-edit-transaction.html",
            account_book=account_book,
            form=form,
        )

    data = form.data.copy()
    data.pop("csrf_token")

    data["date"] = data["date"].isoformat()
    data["value"] = float(data["value"])
    if not transaction:
        transaction = models.CreatedTransaction.from_dict(data)
        response = create_v1_transactions_post.sync(
            client=client, json_body=transaction
        )
    else:
        transaction = models.UpdatedTransaction.from_dict(data)
        response = update_v1_transactions_transaction_id_put.sync(
            client=client, json_body=transaction, transaction_id=transaction_id
        )

    return redirect(url_for("account_books.view", account_book_id=account_book.id))
