from flask import Blueprint, render_template, redirect, url_for
import datetime

module = Blueprint("site", __name__)


@module.route("/")
def index():
    return render_template("/sites/index.html")
