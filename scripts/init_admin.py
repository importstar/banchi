import sys

from banchiapi import models
import datetime
import asyncio


async def create_user_admin():
    class Setting:
        def __init__(self):
            self.MONGODB_URI = "mongodb://localhost/banchidb"

    settings = Setting()
    if len(sys.argv) > 1:
        settings.MONGODB_URI = "mongodb://mongodb/banchidb"

    await models.init_beanie(None, settings)

    print("start check admin")
    user = await models.users.User.find_one(models.users.User.username == "admin")

    if user:
        print("Found admin user", user)
        return
    print("end check admin")

    print("start create admin")
    user = models.users.User(
        email="admin@example.com",
        username="admin",
        password="",
        first_name="admin",
        last_name="system",
        roles=["user", "admin"],
    )
    await user.set_password("p@ssw0rd")
    await user.save()
    print("finish")


if __name__ == "__main__":
    asyncio.run(create_user_admin())
