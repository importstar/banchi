import flet

from . import accounts, dashboard


def register_views(app):
    troute = flet.TemplateRoute(app.page.route)
    accounts.register_views(app, troute)
    dashboard.register_views(app, troute)
