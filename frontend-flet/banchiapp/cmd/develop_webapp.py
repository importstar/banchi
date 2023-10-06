import flet
import os

from banchiapp import app

DEFAULT_FLET_PATH = ""
DEFAULT_FLET_PORT = 8081


if __name__ == "__main__":
    flet_path = os.getenv("FLET_PATH", DEFAULT_FLET_PATH)
    flet_port = int(os.getenv("FLET_PORT", DEFAULT_FLET_PORT))
    flet.app(
        name=flet_path,
        port=flet_port,
        target=app.main,
        view=flet.WEB_BROWSER,
    )
    # flet.app(port=8080, target=app.main, view=None, recursive="banchiapp")
