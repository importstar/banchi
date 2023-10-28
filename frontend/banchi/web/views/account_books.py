from flask import Blueprint, render_template, redirect, url_for
import datetime

module = Blueprint("account_books", __name__, url_prefix="/account_books")


@module.route("")
def index():
    return render_template("/account_books/index.html")
