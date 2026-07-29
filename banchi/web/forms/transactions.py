import datetime
from wtforms import validators, fields, widgets

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed

from .fields import TagListField

from banchi_client import models


class TransactionForm(FlaskForm):
    date = fields.DateTimeField(
        "Date",
        format=[
            "%d/%m/%Y %H:%M",
            "%d/%m/%Y %H:%M:%S",
            "%Y-%m-%dT%H:%M",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
        ],
        widget=widgets.TextInput(),
        default=datetime.datetime.now,
    )
    from_account_book_id = fields.SelectField("From Account Book")
    to_account_book_id = fields.SelectField("To Account Book")
    description_ = fields.StringField("Description")

    value = fields.DecimalField(
        "Value", validators=[validators.InputRequired()], default=0, places=2
    )

    currency = fields.SelectField(
        "Currency",
        validators=[validators.InputRequired()],
        choices=[(e.value, e.value.upper()) for e in models.CurrencyEnum],
    )

    tags = TagListField("Tags")
    remarks = fields.TextAreaField("Remarks")


class TransactionListForm(FlaskForm):
    transactions = fields.FieldList(
        fields.FormField(TransactionForm),
        min_entries=1,
        max_entries=10,
        validators=[validators.Optional()],
    )


class TransactionTemplateForm(TransactionListForm):
    name = fields.StringField("Name", validators=[validators.InputRequired()])


class ApplyTransactionTemplateForm(FlaskForm):
    date = fields.DateTimeField(
        "Date",
        format=[
            "%d/%m/%Y %H:%M",
            "%d/%m/%Y %H:%M:%S",
            "%Y-%m-%dT%H:%M",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
        ],
        widget=widgets.TextInput(),
        default=datetime.datetime.now,
    )
