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


class AccountBookForm(FlaskForm):
    name = fields.StringField(
        "Name", validators=[validators.InputRequired(), validators.Length(min=3)]
    )
    parent_id = fields.SelectField(
        "Parent",
        validators=[validators.InputRequired()],
        choices=[("-", "เป็นระดับแรก")],
    )
    description = fields.TextAreaField("Description", validators=[])
    type = fields.SelectField(
        "Type",
        validators=[validators.InputRequired()],
        choices=[(e.value, e.value.title()) for e in models.AccountTypeEnum],
    )
    smallest_fraction = fields.SelectField(
        "Smallest Fraction",
        validators=[validators.InputRequired()],
        choices=[(e.value, 1 / e.value) for e in models.SmallestFractionEnum],
        default=100,
        coerce=int,
    )
    currency = fields.SelectField(
        "Currency",
        validators=[validators.InputRequired()],
        choices=[(e.value, e.value.upper()) for e in models.CurrencyEnum],
    )
