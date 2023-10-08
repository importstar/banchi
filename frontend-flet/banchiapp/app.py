import flet

import pages


class BanchiApp:
    def __init__(self, page: flet.Page):
        self.page = page

        self.login = pages.accounts.login.Login()
        self.register = pages.accounts.register.Register()
        self.private = pages.dashboard.private.PrivagePage()
        self.dashboard = pages.dashboard.default.DashboardView()

        print("--->", page.route)

        page.on_route_change = self.route_change
        # page.on_view_pop = self.view_pop
        # page.go(page.route)

        self.appbar = flet.AppBar(
            leading=flet.Icon(flet.icons.PALETTE),
            leading_width=40,
            title=flet.Text("AppBar Example"),
            center_title=False,
            bgcolor=flet.colors.SURFACE_VARIANT,
            actions=[
                flet.IconButton(flet.icons.WB_SUNNY_OUTLINED),
                flet.IconButton(flet.icons.FILTER_3),
                flet.PopupMenuButton(
                    items=[
                        flet.PopupMenuItem(text="Item 1"),
                        flet.PopupMenuItem(),  # divider
                        flet.PopupMenuItem(
                            text="Checked item",
                            checked=False,
                            on_click=self.check_item_clicked,
                        ),
                    ]
                ),
            ],
        )

    def check_item_clicked(self, e):
        e.control.checked = not e.control.checked
        self.page.update()

    def initial(self):
        self.page.views.clear()

        self.page.views.append(
            flet.View(
                "/login",
                [self.login],
            )
        )
        # self.page.views.append(
        #     flet.View(
        #         "/register",
        #         [self.register],
        #     )
        # )

        self.page.views.append(
            flet.View(
                "/dashboard",
                [self.appbar, self.dashboard],
            )
        )

        # self.page.add(self.dashboard)
        # self.dashboard.initialize()

        # create an initial board for demonstration if no boards
        # if len(self.boards) == 0:
        #     self.create_new_board("My First Board")
        self.page.go("/dashboard")
        self.page.update()

    def route_change(self, route):
        troute = flet.TemplateRoute(self.page.route)

        if troute.match("/"):
            self.page.go("/login")
        # elif troute.match("/board/:id"):
        #     if int(troute.id) > len(self.store.get_boards()):
        #         self.page.go("/")
        #         return
        #     self.layout.set_board_view(int(troute.id))
        # elif troute.match("/boards"):
        #     self.layout.set_all_boards_view()
        # elif troute.match("/members"):
        #     self.layout.set_members_view()

        self.page.update()

    #     self.page.views.clear()
    #     self.page.views.append(flet.View("/", [self.login]))
    #     # page.views.append(flet.View("/register", [register]))
    #     # page.views.append(flet.View("/private", [private]))

    #     # page.add(flet.Text("Body!"))

    #     if self.page.route == "/private":
    #         if self.page.session.get("login") == None:
    #             # self.page.views.append(flet.View("/", [self.login]))
    #             self.page.go("/")
    #         else:
    #             self.page.views.append(flet.View("/private", [self.private]))

    #     self.page.update()

    # def view_pop(self, view):
    #     # self.page.views.pop()
    #     # top_view = self.page.views[-1]
    #     # self.page.go(top_view.route)
    #     print("view>", view)


def main(page: flet.Page):
    app = BanchiApp(page)
    app.initial()


# use for flet run
if __name__ == "__main__":
    flet.app(target=main, assets_dir="assets")
