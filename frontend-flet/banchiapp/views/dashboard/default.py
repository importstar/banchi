import flet
from ..base import base


class DashboardView(base.BaseView):
    # def __init__(self, page):
    #     super().__init__(page)
    def __init__(self, app):
        super().__init__(app)

    # def build(self):
    #     return flet.Container(
    #         content=flet.Column(
    #             [
    #                 flet.Text("This is private page", size=30),
    #                 flet.ElevatedButton("Logout", on_click=self.logout),
    #             ]
    #         )
    #     )

    # def logout(self, e):
    #     self.page.session.clear()
    #     self.page.go("/")
    #     self.page.update()
