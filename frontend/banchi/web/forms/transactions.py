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
    from_account_book_id = fields.SelectField("From Account Book")
    to_account_book_id = fields.SelectField("To Account Book")
    description = fields.StringField(
        "Description", validators=[validators.InputRequired()]
    )
    value = fields.FloatField("Value", validators=[validators.InputRequired()])
