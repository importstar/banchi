"""
Created on Oct 13, 2013

@author: boatkrap
"""

from wtforms import validators
from wtforms import fields

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed

from .. import models
from .fields import TagListField


class LoginForm(FlaskForm):
    username = fields.StringField(
        "Username", validators=[validators.InputRequired(), validators.Length(min=3)]
    )
    password = fields.PasswordField(
        "Password", validators=[validators.InputRequired(), validators.Length(min=3)]
    )
