from flask import Blueprint, render_template, redirect, url_for
import datetime

module = Blueprint("accounts", __name__, url_prefix="/accounts")


@module.route("")
def index():
    return render_template("/accounts/index.html")
