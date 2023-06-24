import mongoengine as me

# must remove after understand flow
from .users import User, Address
from .customers import Customer, ReferenceCustomerInformation
from .request_logs import RequestLog
from .system_settings import (
    SystemSetting,
)
from .costs import Cost
from .divisions import Division, DivisionCost
from .bills import Bill, ReferenceBillInformation
from .receipts import Receipt
from .organizations import Organization
from .system_settings import AuthorizedSignatory

__all__ = [
    "User",
    "Customer",
    "Address",
    "RequestLog" "Cost",
    "Bill",
    "Receipt",
    "SystemSetting",
    "Division",
    "DivisionCost",
    "Organization",
    "AuthorizedSignatory",
]


def init_mongoengine(settings):
    dbname = settings.MONGODB_DB
    host = settings.MONGODB_HOST
    port = settings.MONGODB_PORT
    username = settings.MONGODB_USERNAME
    password = settings.MONGODB_PASSWORD

    me.connect(db=dbname, host=host, port=port, username=username, password=password)
