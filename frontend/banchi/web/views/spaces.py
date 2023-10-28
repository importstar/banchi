from flask import Blueprint, render_template, redirect, url_for
import datetime

module = Blueprint("spaces", __name__, url_prefix="/spaces")


@module.route("")
def index():
    return render_template("/spaces/index.html")


@module.route("/create", defaults=dict(space_id=None), methods=["GET", "POST"])
@module.route("/<space_id>/edit", methods=["GET", "POST"])
def create_or_edit(space_id):
    return render_template("/spaces/index.html")
