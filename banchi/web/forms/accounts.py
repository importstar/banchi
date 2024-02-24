"""
Created on Oct 13, 2013

@author: boatkrap
"""

from wtforms import validators
from wtforms import fields

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed

from .fields import TagListField


class AccountForm(FlaskForm):
    name = fields.StringField(
        "Name", validators=[validators.InputRequired(), validators.Length(min=3)]
    )
    description = fields.TextAreaField("Description", validators=[])
    currency = fields.SelectField(
        "Curency", validators=[validators.InputRequired()], choices=["THB"]
    )
