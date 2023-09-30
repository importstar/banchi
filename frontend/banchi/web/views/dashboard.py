from flask import Blueprint, render_template
from flask_login import login_required, current_user

from viyyoor import models
import mongoengine as me
from viyyoor.web import acl

from .. import redis_rq

import datetime

module = Blueprint("dashboard", __name__, url_prefix="/dashboard")
subviews = []


def index_admin():
    now = datetime.datetime.now()
    endorser_positions = models.classes.ENDORSER_POSITIONS
    # queries = {
    #     f"endorsers__{ep[0]}__user": current_user._get_current_object()
    #     for ep in endorser_positions
    # }
    # print("q", queries)
    classes_set = set()
    endorsed_query = dict()

    for ep in endorser_positions:
        queries = {f"endorsers__{ep[0]}__user": current_user._get_current_object()}
        endorsed_query[
            f"endorsements__{ep[0]}__endorser"
        ] = current_user._get_current_object()
        sub_classes = models.Class.objects(**queries)
        classes_set.update(sub_classes)

    classes = list(classes_set)

    query_obj = None
    for k, v in endorsed_query.items():
        if query_obj:
            query_obj = query_obj | me.Q(**{k: v})
        else:
            query_obj = me.Q(**{k: v})

    endorsed_classes = models.Certificate.objects(
        query_obj,
        class___in=classes + [current_user.get_current_organization()],
    ).distinct(field="class_")

    endorsed_classes = list(filter(lambda c: c.status == "active", endorsed_classes))

    endorsed_classes.sort(key=lambda c: c.id, reverse=True)

    endorsed_jobs = dict()
    redis_queue = redis_rq.redis_queue
    for c in endorsed_classes:
        endorsed_jobs[str(c.id)] = redis_queue.get_job(
            f"endorsements_certificates_{c.id}"
        )

    return render_template(
        "/dashboard/index-admin.html",
        now=datetime.datetime.now(),
        endorsed_classes=endorsed_classes,
        endorsed_jobs=endorsed_jobs,
    )


def index_endorser():
    now = datetime.datetime.now()
    endorser_positions = models.classes.ENDORSER_POSITIONS
    # queries = {
    #     f"endorsers__{ep[0]}__user": current_user._get_current_object()
    #     for ep in endorser_positions
    # }
    # print("q", queries)
    classes_set = set()
    endorsed_query = dict()

    for ep in endorser_positions:
        queries = {f"endorsers__{ep[0]}__user": current_user._get_current_object()}
        endorsed_query[
            f"endorsements__{ep[0]}__endorser"
        ] = current_user._get_current_object()
        sub_classes = models.Class.objects(**queries)
        classes_set.update(sub_classes)

    classes = list(classes_set)

    query_obj = None
    for k, v in endorsed_query.items():
        if query_obj:
            query_obj = query_obj | me.Q(**{k: v})
        else:
            query_obj = me.Q(**{k: v})

    endorsed_classes = models.Certificate.objects(
        query_obj,
        class___in=classes + [current_user.get_current_organization()],
    ).distinct(field="class_")

    endorsed_classes = list(filter(lambda c: c.status == "active", endorsed_classes))

    endorsed_classes.sort(key=lambda c: c.id, reverse=True)

    endorsed_jobs = dict()
    redis_queue = redis_rq.redis_queue
    for c in endorsed_classes:
        endorsed_jobs[str(c.id)] = redis_queue.get_job(
            f"endorsements_certificates_{c.id}"
        )

    return render_template(
        "/dashboard/index-endorser.html",
        now=datetime.datetime.now(),
        endorsed_classes=endorsed_classes,
        endorsed_jobs=endorsed_jobs,
    )


def index_user():
    certificates = models.Certificate.objects(
        me.Q(common_id=current_user.username)
        | me.Q(common_id=current_user.citizen_id)
        | me.Q(common_id__in=current_user.other_ids),
        status="completed",
    ).order_by("-id")
    now = datetime.datetime.now()
    return render_template(
        "/dashboard/index-user.html",
        now=datetime.datetime.now(),
        certificates=certificates,
    )


@module.route("/")
@login_required
def index():
    user = current_user._get_current_object()
    if user.has_roles("admin") or user.has_organization_roles("staff", "admin"):
        return index_admin()

    elif user.has_organization_roles("endorser"):
        return index_endorser()

    return index_user()


@module.route("/me")
@login_required
def show_my_certificates():
    return index_user()


@module.route("/endorsements")
@login_required
def show_endorsements():
    endorser_positions = models.classes.ENDORSER_POSITIONS
    classes_set = set()
    endorsed_query = dict()
    endorses_query = dict()

    for ep in endorser_positions:
        queries = {f"endorsers__{ep[0]}__user": current_user._get_current_object()}
        endorsed_query[
            f"endorsements__{ep[0]}__endorser"
        ] = current_user._get_current_object()
        endorses_query[
            f"endorsements__{ep[0]}__endorser__ne"
        ] = current_user._get_current_object()
        sub_classes = models.Class.objects(**queries)
        classes_set.update(sub_classes)

    classes = list(classes_set)
    endorses_classes = models.Certificate.objects(
        status="prerelease", class___in=classes, **endorses_query
    ).distinct(field="class_")

    query_obj = None
    for k, v in endorsed_query.items():
        if query_obj:
            query_obj = query_obj | me.Q(**{k: v})
        else:
            query_obj = me.Q(**{k: v})

    endorsed_classes = models.Certificate.objects(
        query_obj, class___in=classes
    ).distinct(field="class_")

    endorsed_classes = list(filter(lambda c: c.status == "active", endorsed_classes))
    endorses_classes = list(filter(lambda c: c.status == "active", endorses_classes))

    endorses_classes.sort(key=lambda c: c.id, reverse=True)
    endorsed_classes.sort(key=lambda c: c.id, reverse=True)

    endorsed_jobs = dict()
    redis_queue = redis_rq.redis_queue
    for c in endorsed_classes:
        endorsed_jobs[str(c.id)] = redis_queue.get_job(
            f"endorsements_certificates_{c.id}"
        )

    return render_template(
        "/dashboard/endorsements.html",
        endorses_classes=endorses_classes,
        endorsed_classes=endorsed_classes,
        endorsed_jobs=endorsed_jobs,
    )
