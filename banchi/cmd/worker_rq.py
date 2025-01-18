from banchi import worker


def main():
    rq_server = worker.create_server()
    rq_server.run()
