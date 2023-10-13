import flet


class PrivagePage(flet.UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        return flet.container(
            content=flet.Column(
                [
                    flet.Text("This is private page", size=30),
                    flet.ElevateButton("Logout", on_click=self.logout),
                ]
            )
        )

    def logout(self, e):
        self.page.session.clear()
        self.page.go("/")
        self.page.update()
