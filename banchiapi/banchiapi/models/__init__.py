import sys
from typing import Sequence, Type, TypeVar
from inspect import getmembers, isclass
import motor
import beanie


DocType = TypeVar("DocType", bound=beanie.Document)


# must remove after understand flow
from .users import User


async def gather_documents() -> Sequence[Type[DocType]]:
    """Returns a list of all MongoDB document models defined in `models` module."""
    return [
        doc
        for _, doc in getmembers(sys.modules[__name__], isclass)
        if issubclass(doc, beanie.Document) and doc.__name__ != "Document"
    ]


class BeanieClient:
    async def init_beanie(self, settings):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URI)

        await beanie.init_beanie(
            database=self.client.db_name, document_models=await gather_documents()
        )


async def init_beanie(app, settings):
    await beanie_client.init_beanie(settings)


beanie_client = BeanieClient()
