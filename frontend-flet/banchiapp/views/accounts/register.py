import flet


class Register(flet.UserControl):
    def __init__(self, app):
        super().__init__()
        self.username = flet.TextField(label="Username")
        self.password = flet.TextField(label="Password")

        self.app = app

    def build(self):
        return flet.Container(
            content=flet.Column(
                [
                    flet.Text("Register", size=30),
                    self.username,
                    self.password,
                    flet.ElevatedButton("Register", on_click=self.register),
                ]
            )
        )

    def register(self, e):
        print("register success", self.username.value, self.password.value)
        self.app.page.go("/")
        self.app.page.update()
