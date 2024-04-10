import datetime
from wtforms import validators, fields, widgets

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed

from .fields import TagListField

from banchi_client import models


class TransactionForm(FlaskForm):
    date = fields.DateTimeField(
        "Date",
        format="%Y-%m-%d %H:%M:%S",
        widget=widgets.TextInput(),
        default=datetime.datetime.now,
    )
    from_account_book_id = fields.SelectField("From Account Book")
    to_account_book_id = fields.SelectField("To Account Book")
    description = fields.StringField(
        "Description", validators=[validators.InputRequired()]
    )

    value = fields.DecimalField(
        "Value", validators=[validators.InputRequired()], default=0, places=2
    )

    currency = fields.SelectField(
        "Currency",
        validators=[validators.InputRequired()],
        choices=[(e.value, e.value.upper()) for e in models.CurrencyEnum],
    )

    tags = fields.SelectMultipleField("Tags", choices=[], validate_choice=False)
