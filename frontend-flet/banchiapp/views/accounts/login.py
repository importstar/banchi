import flet


class Login(flet.UserControl):
    def __init__(self, app):
        super().__init__()
        self.username = flet.TextField(label="Username")
        self.password = flet.TextField(label="Password")

        self.app = app

    def build(self):
        return flet.Container(
            content=flet.Column(
                [
                    flet.Text("Banchi Login", size=30),
                    self.username,
                    self.password,
                    flet.ElevatedButton("Login", on_click=self.do_login),
                    flet.TextButton("No Have Account", on_click=self.register),
                ]
            )
        )

    def do_login(self, e):
        if self.username.value == "admin" and self.password.value == "password":
            print("success")
            data_login = dict(value=True, username=self.username.value)
            self.page.session.set("login", data_login)
            self.page.go("/private")
            self.page.update()
        else:
            print("wrong")
            self.page.snack_bar = flet.SnackBar(flet.Text("Wrong Login", size=30))
            self.page.snack_bar.open = True
            self.page.update()

    def register(self, e):
        self.app.page.go("/register")
        self.app.page.update()
