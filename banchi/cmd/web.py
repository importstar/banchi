from banchi import web

from livereload import Server


def main():
    options = web.get_program_options()
    app = web.create_app()
    app.debug = options.debug

    server = Server(app.wsgi_app)
    server.watch("banchi/web")
    server.serve(
        debug=options.debug,
        host=options.host,
        port=int(options.port),
        restart_delay=2,
        # open_url_delay=7,
    )

    # app.run(debug=options.debug, host=options.host, port=int(options.port))
