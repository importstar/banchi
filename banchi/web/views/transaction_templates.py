from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
import datetime
import decimal
from collections import OrderedDict


from banchi_client import models
from banchi_client.api.v1 import (
    get_all_v1_transaction_templates_get,
    get_v1_transaction_templates_transaction_template_id_get,
    create_v1_transaction_templates_post,
    update_v1_transaction_templates_transaction_template_id_put,
    delete_v1_transaction_templates_transaction_template_id_delete,
    get_all_v1_account_books_get,
    get_v1_account_books_account_book_id_get,
    create_v1_transactions_post,
)

from .. import banchi_api_clients
from .. import forms
from .. import utils

module = Blueprint(
    "transaction_templates", __name__, url_prefix="/transaction-templates"
)


@module.route("")
@login_required
def index():
    account_id = request.args.get("account_id")
    client = banchi_api_clients.client.get_current_client()
    response = get_all_v1_transaction_templates_get.sync(
        client=client,
        account_id=account_id,
    )

    return render_template(
        "/transaction_templates/index.html",
        transaction_templates=response.transaction_templates,
    )


@module.route(
    "/add",
    methods=["GET", "POST"],
    defaults=dict(transaction_template_id=None),
)
@module.route("/<transaction_template_id>/edit", methods=["GET", "POST"])
@login_required
def add_or_edit(transaction_template_id):
    client = banchi_api_clients.client.get_current_client()

    account_id = request.args.get("account_id", None)

    response = get_all_v1_account_books_get.sync(client=client, account_id=account_id)

    account_books = response.account_books

    form = forms.transactions.TransactionTemplateForm()

    display_names = utils.account_books.get_display_names(
        account_books, excluse_none_parent=True
    )
    account_book_choices = [
        (str(ab.id), display_names[ab.id])
        for ab in account_books
        if ab.id in display_names
    ]

    account_book_choices = sorted(
        account_book_choices,
        key=lambda abn: abn[1],
    )

    transaction_template = None
    if transaction_template_id and request.method == "GET":
        transaction_template = (
            get_v1_transaction_templates_transaction_template_id_get.sync(
                client=client, transaction_template_id=transaction_template_id
            )
        )

        data = transaction_template.to_dict()
        for transaction in data["transactions"]:
            transaction["value"] = decimal.Decimal(transaction["value"])
            transaction["description_"] = transaction["description"]

        form = forms.transactions.TransactionTemplateForm(data=data)

    elif request.method == "GET" and not transaction_template_id:
        [form.transactions.append_entry() for _ in range(9)]

    for sub_form in form.transactions:
        sub_form.to_account_book_id.choices = account_book_choices
        sub_form.from_account_book_id.choices = account_book_choices

    if not form.validate_on_submit():

        return render_template(
            "/transaction_templates/add-or-edit-transaction-template.html",
            # account_book=account_book,
            form=form,
        )

    transactions = []
    for sub_form in form.transactions:
        sub_data = sub_form.data.copy()
        sub_data.pop("csrf_token")
        sub_data["value"] = float(sub_data["value"])
        sub_data["date"] = sub_data["date"].isoformat()
        sub_data["description"] = sub_data["description_"]

        transactions.append(sub_data)

    data = dict(transactions=transactions, name=form.name.data)

    if transaction_template_id:
        updated_transaction_template = models.UpdatedTransactionTemplate.from_dict(data)
        response = update_v1_transaction_templates_transaction_template_id_put.sync(
            client=client,
            account_id=account_id,
            transaction_template_id=transaction_template_id,
            body=updated_transaction_template,
        )
    else:
        created_transaction_template = models.CreatedTransactionTemplate.from_dict(data)
        # print("==>",created_transaction_template)
        response = create_v1_transaction_templates_post.sync(
            client=client,
            body=created_transaction_template,
            account_id=account_id,
        )

    return redirect(url_for("transaction_templates.index", account_id=account_id))


@module.route("/<transaction_template_id>/select-apply-date", methods=["GET", "POST"])
@login_required
def select_apply_date(transaction_template_id):
    account_id = request.args.get("account_id", None)

    form = forms.transactions.ApplyTransactionTemplateForm()
    if not form.validate_on_submit():
        return render_template(
            "/transaction_templates/select-apply-date.html",
            form=form,
        )

    return redirect(
        url_for(
            "transaction_templates.apply",
            transaction_template_id=transaction_template_id,
            account_id=account_id,
            date=form.date.data.isoformat(),
        )
    )


@module.route("/<transaction_template_id>/apply", methods=["GET", "POST"])
@login_required
def apply(transaction_template_id):

    client = banchi_api_clients.client.get_current_client()
    account_id = request.args.get("account_id", None)

    date_str = request.args.get("date", None)
    date = datetime.datetime.now()
    if date_str:
        date = datetime.datetime.fromisoformat(date_str)

    response = get_all_v1_account_books_get.sync(client=client, account_id=account_id)
    account_books = response.account_books

    form = forms.transactions.TransactionListForm()

    display_names = utils.account_books.get_display_names(
        account_books, excluse_none_parent=True
    )
    account_book_choices = [
        (str(ab.id), display_names[ab.id])
        for ab in account_books
        if ab.id in display_names
    ]

    account_book_choices = sorted(
        account_book_choices,
        key=lambda abn: abn[1],
    )

    transaction_template = None
    if transaction_template_id and request.method == "GET":
        transaction_template = (
            get_v1_transaction_templates_transaction_template_id_get.sync(
                client=client, transaction_template_id=transaction_template_id
            )
        )

        data = transaction_template.to_dict()
        for transaction in data["transactions"]:
            transaction["value"] = decimal.Decimal(transaction["value"])
            transaction["description_"] = transaction["description"]
            transaction["date"] = date

        form = forms.transactions.TransactionListForm(data=data)

    for sub_form in form.transactions:
        sub_form.to_account_book_id.choices = account_book_choices
        sub_form.from_account_book_id.choices = account_book_choices

    if not form.validate_on_submit():

        return render_template(
            "/transaction_templates/apply-transaction.html",
            form=form,
        )

    for idx, sub_form in enumerate(form.transactions):
        if (
            not sub_form.data
            or not sub_form.date.data
            or (
                not sub_form.data.get("description_", "").strip()
                or not sub_form.data.get("value", 0)
            )
        ):
            continue

        entry_data = sub_form.data.copy()
        entry_data.pop("csrf_token")
        entry_data["date"] = entry_data["date"].isoformat()
        entry_data["value"] = float(entry_data["value"])
        entry_data["description"] = entry_data["description_"]

        transaction = models.CreatedTransaction.from_dict(entry_data)

        response = create_v1_transactions_post.sync(client=client, body=transaction)

    account_book_id = sub_form.from_account_book_id.data

    return redirect(url_for("account_books.view", account_book_id=account_book_id))


@module.route("/<transaction_template_id>/delete")
@login_required
def delete(transaction_template_id):
    client = banchi_api_clients.client.get_current_client()
    transaction = delete_v1_transaction_templates_transaction_template_id_delete.sync(
        client=client, transaction_id=transaction_template_id
    )

    account_id = request.args.get("account_id", None)

    return redirect(url_for("transaction_templates.index", account_id=account_id))
