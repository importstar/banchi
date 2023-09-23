import flet
import os


DEFAULT_FLET_PATH = ""  # or 'ui/path'
DEFAULT_FLET_PORT = 8550


# async def main(page: flet.Page):
#     await page.add_async(flet.Text("Hello, async world! xxxx"))

#     await page.add_async(flet.Text(f"Initial route: {page.route}"))

#     async def route_change(e):
#         await page.add_async(Text(f"New route: {e.route}"))

#     page.on_route_change = route_change
#     await page.update_async()

import flet as ft


async def main(page: flet.Page):
    page.title = "Routes Example"

    async def route_change(route):
        page.views.clear()

        async def go_store(e):
            await page.go_async("/store")

        async def go_home(e):
            await page.go_async("/")

        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(
                        title=ft.Text("Flet app"), bgcolor=ft.colors.SURFACE_VARIANT
                    ),
                    ft.ElevatedButton("Visit Store", on_click=go_store),
                ],
            )
        )
        if page.route == "/store":
            page.views.append(
                ft.View(
                    "/store",
                    [
                        ft.AppBar(
                            title=ft.Text("Store"), bgcolor=ft.colors.SURFACE_VARIANT
                        ),
                        ft.ElevatedButton("Go Home", on_click=go_home),
                    ],
                )
            )
        await page.update_async()

    async def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        await page.go_async(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    await page.go_async(page.route)


if __name__ == "__main__":
    flet_path = os.getenv("FLET_PATH", DEFAULT_FLET_PATH)
    flet_port = int(os.getenv("FLET_PORT", DEFAULT_FLET_PORT))
    print("FLET_PATH:", flet_path)
    print("FLET_PORT:", flet_port)
    flet.app(
        name=flet_path,
        port=flet_port,
        target=main,
        view=flet.WEB_BROWSER,
        route_url_strategy="hash",
    )
