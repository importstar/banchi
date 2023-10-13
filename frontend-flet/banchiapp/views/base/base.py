import flet
from flet import (
    AlertDialog,
    AppBar,
    Column,
    Container,
    ElevatedButton,
    Icon,
    Page,
    PopupMenuButton,
    PopupMenuItem,
    RoundedRectangleBorder,
    Row,
    TemplateRoute,
    Text,
    TextField,
    UserControl,
    View,
    colors,
    icons,
    margin,
    padding,
    theme,
)


class BaseView(UserControl):
    # def __init__(self, page: Page):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def build(self):
        # self.layout = AppLayout(
        #     self,
        #     # self.page,
        #     self.store,
        #     tight=True,
        #     expand=True,
        #     vertical_alignment="start",
        # )
        # print("hear", self.layout)
        return flet.Text("Banchi Dashboard", size=30)

    def initialize(self):
        pass
        # self.page.views.clear()
        # self.page.views.append(
        #     View(
        #         "/",
        #         [self.appbar, self.layout],
        #         padding=padding.all(0),
        #         bgcolor=colors.BLUE_GREY_200,
        #     )
        # )
        # self.page.update()
        # # create an initial board for demonstration if no boards
        # if len(self.boards) == 0:
        #     self.create_new_board("My First Board")
        # self.page.go("/")
