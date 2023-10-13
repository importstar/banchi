import flet

from . import login, register


def register_views(app, troute):
    print("-> hear ->", app.page.route)
    if troute.match("/login"):
        app.page.views.append(
            flet.View(
                "/login",
                [login.Login(app)],
            )
        )
    elif troute.match("/register"):
        print("-> hear")
        app.page.views.append(
            flet.View(
                "/register",
                [register.Register(app)],
            )
        )
