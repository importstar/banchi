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

)

from .. import banchi_api_clients
from .. import forms
from .. import utils

module = Blueprint("transaction_templates", __name__, url_prefix="/transaction-templates")


@module.route("")
@login_required
def index():
    account_id = request.args.get("account_id")
    client = banchi_api_clients.client.get_current_client()
    transaction = get_all_v1_transaction_templates_get.sync(
            client=client,
            account_id=account_id,
        )





    return render_template(
        "/transaction_templates/index.html",
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
    account_book = None

    account_id = request.args.get("account_id", None)
    if account_book:
        account_id = account_book.account.id

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

    if request.method == "GET":
        [form.transactions.append_entry() for _ in range(9)]

    for sub_form in form.transactions:
        sub_form.to_account_book_id.choices = account_book_choices
        sub_form.from_account_book_id.choices = account_book_choices

        if request.method == "GET" and account_book:
            sub_form.from_account_book_id.data = str(account_book.id)
            sub_form.to_account_book_id.data = str(account_book.id)

    if not form.validate_on_submit():

        return render_template(
            "/transaction_templates/add-or-edit-transaction-template.html",
            account_book=account_book,
            form=form,
        )
    
    print(form.data)
    data = []
    for sub_form in form.transactions:
        sub_data = sub_form.data.copy()
        sub_data.pop("csrf_token")
        sub_data["value"] = float(sub_data["value"])
        sub_data["date"] = sub_data["date"].isoformat()
        sub_data["description"] = sub_data['description_']

        data.append(sub_data)


    

    if transaction_template_id:
        updated_transaction_template = models.UpdatedTransactionTemplate.from_dict(data)
        response = update_v1_transaction_templates_transaction_template_id_put.sync(
            client=client,
            transaction_template_id=transaction_template_id,
            transaction_template=updated_transaction_template)
    else:
        created_transaction_template = models.CreatedTransactionTemplate.from_dict(dict(transactions=data))
        print(created_transaction_template)
        response = create_v1_transaction_templates_post.sync(
            client=client,
            body=created_transaction_template,
            account_id=account_id,
            )




    return redirect(url_for("transaction_templates.index", account_id=account_id))



@module.route("/<transaction_template_id>/delete")
@login_required
def delete(transaction_template_id):
    client = banchi_api_clients.client.get_current_client()
    transaction = delete_v1_transaction_templates_transaction_id_delete.sync(
        client=client, transaction_id=transaction_id
    )

    account_book_id = transaction.from_account_book.id

    return redirect(url_for("account_books.view", account_book_id=account_book_id))
