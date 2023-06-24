import sys
import mongoengine as me

# import pandas as pd
from banchaiapi import models
import datetime


def create_user_admin():
    print("start create admin")
    organization = models.Organization(
        name="admin", slogan="", tax_id="0905564002794", code="000", phone="0819693002"
    )
    organization.save()
    division = models.Division(name="admin", code="000", organization=organization)
    division.save()
    user = models.User(
        email="admin@example.com",
        username="admin",
        title_name="admin",
        first_name="admin",
        last_name="system",
        citizen_id="0000000000000",
        roles=["user", "admin"],
        birthday=datetime.datetime.now(),
        division=division,
        organization=organization,
    )

    user.set_password("p@ssw0rd")
    user.save()
    print("finish")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        me.connect(db="banchaidb", host=sys.argv[1])
    else:
        me.connect(db="banchaidb")
    print("start check")
    create_user_admin()

    print("end check")
