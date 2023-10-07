import flet


class Login(flet.UserControl):
    def __init__(self):
        super().__init__()
        self.username = flet.TextField(label="Username")
        self.password = flet.TextField(label="Password")

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
        self.page.go("/register")
        self.page.update()


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


class Register(flet.UserControl):
    def __init__(self):
        self.username = flet.TextField(label="Username")
        self.password = flet.TextField(label="Password")

    def build(self):
        return flet.Container(
            Content=flet.Column(
                [
                    flet.Text("Register", size=30),
                    self.username,
                    self.password,
                    ElevatedButton("Register", on_click=self.register),
                ]
            )
        )

    def register(self, e):
        print("register success", self.username.value, self.password.value)
        self.page.go("/")
        self.page.update()


def main(page: flet.Page):
    login = Login()
    private = PrivagePage()
    register = Register()

    def my_route(route):
        page.views.clear()
        page.views.append(flet.View("/", [login]))
        page.views.append(flet.View("/register", [register]))
        page.views.append(flet.View("/private", [private]))

    # if page.route == "/private":
    #     print(page.session.get("login"))

    #     if page.session.get("login") == None:
    #         page.go("/")
    #     else:
    #         page.views.append(flet.View("/private", [private]))

    page.go("/")
    print("hello >>")
    page.views.append(login)
    page.update()


# use for flet run
if __name__ == "__main__":
    flet.app(target=main)
