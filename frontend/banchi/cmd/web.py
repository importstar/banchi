import flet as ft


async def main(page: ft.Page):
    await page.add_async(ft.Text("Hello, async world!"))


if __name__ == "__main__":
    ft.app(main)
