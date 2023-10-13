import flet
from . import default, private


def register_views(app, troute):
    if troute.match("/dashboard"):
        app.page.views.append(
            flet.View("/dashboard", [app.appbar, default.DashboardView(app)])
        )
