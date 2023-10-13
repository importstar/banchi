import flet

try:
    from . import views
except Exception as e:
    import views


class BanchiApp:
    def __init__(self, page: flet.Page):
        self.page = page

        page.on_route_change = self.route_change

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
        # self.page.views.clear()
        # views.register_views(self)
        self.page.update()

    def route_change(self, route):
        self.page.views.clear()
        print("-->", route)
        views.register_views(self)
        if self.page.route == "/":
            self.page.go("/login")

        self.page.update()


def main(page: flet.Page):
    app = BanchiApp(page)
    app.initial()


# use for flet run
if __name__ == "__main__":
    flet.app(target=main, assets_dir="assets")
