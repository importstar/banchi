import flet
import os


DEFAULT_FLET_PATH = ""  # or 'ui/path'
DEFAULT_FLET_PORT = 8550


async def main(page: flet.Page):
    await page.add_async(flet.Text("Hello, async world! xxxx"))


if __name__ == "__main__":
    flet_path = os.getenv("FLET_PATH", DEFAULT_FLET_PATH)
    flet_port = int(os.getenv("FLET_PORT", DEFAULT_FLET_PORT))
    print("FLET_PATH:", flet_path)
    print("FLET_PORT:", flet_port)
    flet.app(name=flet_path, target=main, view=flet.WEB_BROWSER, port=flet_port)
