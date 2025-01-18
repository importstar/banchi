import asyncio
import datetime
import json
import pathlib


import os

import redis
from rq import Worker, Queue, SimpleWorker

from banchi.api import models

import logging

logger = logging.getLogger(__name__)

listen = ["default"]


class ProcessWorker(SimpleWorker):
    def __init__(self, *args, **kwargs):
        settings = kwargs.pop("settings")
        super().__init__(*args, **kwargs)

        models.init_mongoengine(settings)


class WorkerServer:
    def __init__(self, settings):
        self.settings = settings

        redis_url = settings.get("REDIS_URL", "redis://localhost:6379")
        self.conn = redis.from_url(redis_url)

        logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.DEBUG)

    def run(self):
        worker = ProcessWorker(listen, connection=self.conn, settings=self.settings)
