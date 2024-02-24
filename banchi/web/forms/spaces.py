"""
Created on Oct 13, 2013

@author: boatkrap
"""

from wtforms import validators
from wtforms import fields

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed

from .fields import TagListField


class SpaceForm(FlaskForm):
    name = fields.StringField(
        "Name", validators=[validators.InputRequired(), validators.Length(min=3)]
    )
    code = fields.StringField("Code", validators=[])
    tax_id = fields.StringField("Tax ID", validators=[])


class SpaceRoleForm(FlaskForm):
    member_id = fields.SelectField("Member", validators=[validators.InputRequired()])

    role = fields.SelectField(
        "Role",
        validators=[validators.InputRequired()],
        choices=[(role, role.title()) for role in ["owner", "member"]],
    )
