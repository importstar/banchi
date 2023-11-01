"""
Created on Oct 13, 2013

@author: boatkrap
"""

from wtforms import validators
from wtforms import fields

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed

from .fields import TagListField

from banchi_client import models


class TransactionForm(FlaskForm):
    description = fields.TextAreaField("Description", validators=[])
    to_account_book_id = fields.SelectField(
        "To Account Book",
        validators=[validators.InputRequired()],
        choices=[("", "Select Account Book")],
    )

    value = fields.FloatField(
        "Value",
        validators=[validators.InputRequired()],
        default=0,
    )
