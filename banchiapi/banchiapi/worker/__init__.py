from .server import WorkerServer


def create_server():
    from banchiapi.core import config

    settings = config.get_app_settings()
    server = WorkerServer(settings)

    return server
