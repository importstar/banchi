import asyncio
import datetime
import json
import pathlib


import os

import redis
from rq import Worker, Queue, Connection, SimpleWorker

from banchiapi import models

import logging

logger = logging.getLogger(__name__)

listen = ["default"]


# def create_server():
#     from app.core import config

#     settings = config.get_app_settings()
#     server = WorkerServer(settings)

#     return server


class GeneralWorker(SimpleWorker):
    def __init__(self, *args, **kwargs):
        settings = kwargs.pop("settings")
        super().__init__(*args, **kwargs)

         # models.init_mongoengine(settings)


class WorkerServer:
    def __init__(self, settings):
        self.settings = settings

        redis_url = settings.REDIS_URL
        self.conn = redis.from_url(redis_url)

        logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.DEBUG)

    def run(self):
        with Connection(self.conn):
            worker = GeneralWorker(list(map(Queue, listen)), settings=self.settings)
            worker.work()
