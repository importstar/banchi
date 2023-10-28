from flask import Blueprint, render_template, redirect, url_for
import datetime

module = Blueprint("spaces", __name__, url_prefix="/spaces")


@module.route("")
def index():
    return render_template("/spaces/index.html")
