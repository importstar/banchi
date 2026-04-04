import datetime

from flask import (
    Blueprint,
    render_template,
    url_for,
    redirect,
    request,
    session,
    current_app,
    send_file,
    abort,
)
from flask_login import login_user, logout_user, login_required, current_user

from .. import oauth2
from .. import forms

from .. import banchi_api_clients
from .. import models as banchi_web_models

from banchi_client import models
from banchi_client.api.v1 import (
    authentication_v1_auth_login_post,
    get_me_v1_users_me_get,
)


module = Blueprint("users", __name__)


@module.route("/login", methods=("GET", "POST"))
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if "next" in request.args:
        session["next"] = request.args.get("next", None)

    oauth_clients = current_app.extensions["authlib.integrations.flask_client"]._clients

    form = forms.users.LoginForm()

    return render_template("/users/login.html", oauth_clients=oauth_clients, form=form)


@module.route("/login/<name>")
def login_oauth(name):
    client = oauth2.oauth2_client

    scheme = request.environ.get("HTTP_X_FORWARDED_PROTO", "http")
    redirect_uri = url_for(
        "users.authorized_oauth", name=name, _external=True, _scheme=scheme
    )
    response = None
    if name == "google":
        response = client.google.authorize_redirect(redirect_uri)
    elif name == "facebook":
        response = client.facebook.authorize_redirect(redirect_uri)
    elif name == "line":
        response = client.line.authorize_redirect(redirect_uri)
    elif name == "psu":
        response = client.psu.authorize_redirect(redirect_uri)
    elif name == "engpsu":
        response = client.engpsu.authorize_redirect(redirect_uri)
    return response


@module.route("/auth/banchi", methods=["POST"])
def authorized_banchi():
    form = forms.users.LoginForm()
    if not form.validate_on_submit():
        return redirect("users.login")

    username = form.username.data
    password = form.password.data

    model = (
        models.body_authentication_v1_auth_login_post.BodyAuthenticationV1AuthLoginPost(
            username=username, password=password
        )
    )

    client = banchi_api_clients.client.get_current_client(is_anonymous=True)
    response = authentication_v1_auth_login_post.sync(client=client, body=model)

    if not response:
        return redirect(url_for("users.login"))

    session["tokens"] = response.to_dict()

    client = banchi_api_clients.client.get_current_client()
    response = get_me_v1_users_me_get.sync(client=client)

    user = banchi_web_models.users.User(response.to_dict())
    login_user(user)
    session["me"] = response.to_dict()

    return redirect(url_for("dashboard.index"))


@module.route("/auth/<name>")
def authorized_oauth(name):
    client = oauth2.oauth2_client
    remote = None
    try:
        if name == "google":
            remote = client.google
        elif name == "facebook":
            remote = client.facebook
        elif name == "line":
            remote = client.line
        elif name == "psu":
            remote = client.psu
        elif name == "engpsu":
            remote = client.engpsu

        token = remote.authorize_access_token()

    except Exception as e:
        print("autorize access error =>", e)
        return redirect(url_for("users.login"))

    session["oauth_provider"] = name
    return oauth2.handle_authorized_oauth2(remote, token)


@module.route("/logout")
@login_required
def logout():
    name = session.get("oauth_provider")
    logout_user()
    session.clear()

    client = oauth2.oauth2_client
    remote = None
    logout_url = None
    if name == "google":
        remote = client.google
        logout_url = f"{ remote.server_metadata.get('end_session_endpoint') }?redirect={ request.scheme }://{ request.host }"
    elif name == "facebook":
        remote = client.facebook
    elif name == "line":
        remote = client.line
    elif name == "psu":
        remote = client.psu
        logout_url = f"{ remote.server_metadata.get('end_session_endpoint') }"
    elif name == "engpsu":
        remote = client.engpsu

    if logout_url:
        return redirect(logout_url)

    return redirect(url_for("site.index"))


@module.route("/users/<user_id>")
@login_required
def profile(user_id):
    return index()


@module.route("/users", methods=["GET", "POST"])
@login_required
def index():
    biography = ""
    # if current_user.biography:
    #     biography = markdown.markdown(current_user.biography)

    # form = forms.users.SelectOrganizationForm(obj=current_user.user_setting)
    # form.current_organization.choices = [
    #     (str(o.id), o.name) for o in current_user.organizations
    # ]

    # if form.validate_on_submit():
    # current_user.user_setting.current_organization = (
    #     models.Organization.objects.get(id=form.current_organization.data)
    # )
    # current_user.save()
    # return redirect(url_for("users.index"))

    # current_organization = current_user.user_setting.current_organization
    # if current_organization:
    #     form.current_organization.data = str(current_organization.id)

    form = forms.users.UserForm()
    return render_template(
        "/users/index.html", user=current_user, biography=biography, form=form
    )


@module.route("/users/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = forms.users.ProfileForm(obj=current_user, pic=current_user.picture)
    if not form.validate_on_submit():
        return render_template("/users/edit-profile.html", form=form)

    user = current_user._get_current_object()
    form.populate_obj(user)

    if form.pic.data:
        if user.picture:
            user.picture.replace(
                form.pic.data,
                filename=form.pic.data.filename,
                content_type=form.pic.data.content_type,
            )
        else:
            user.picture.put(
                form.pic.data,
                filename=form.pic.data.filename,
                content_type=form.pic.data.content_type,
            )

    user.updated_date = datetime.datetime.now()
    user.save()

    return redirect(url_for("users.index"))


@module.route("/users/<user_id>/picture/<filename>", methods=["GET", "POST"])
@login_required
def picture(user_id, filename):
    user = models.User.objects.get(id=user_id)

    if not user or not user.picture or user.picture.filename != filename:
        return abort(403)

    response = send_file(
        user.picture,
        download_name=user.picture.filename,
        mimetype=user.picture.content_type,
    )
    return response


@module.route(
    "/users/<user_id>/add-signature",
    methods=["GET", "POST"],
    defaults={"signature_id": None},
)
@module.route("/users/<user_id>/signatures/<signature_id>", methods=["GET", "POST"])
@login_required
def add_or_edit_signature(user_id, signature_id):
    user = models.User.objects.get(id=user_id)

    form = forms.signatures.SignatureForm()
    if signature_id:
        signature = models.Signature.objects(id=signature_id).first()
        form = forms.signatures.SignatureForm(obj=signature)

    if not form.validate_on_submit():
        return render_template(
            "/users/add-signature.html",
            form=form,
        )

    if not signature_id:
        signature = models.Signature(
            owner=current_user._get_current_object(),
            ip_address=request.remote_addr,
        )

        signature.file.put(
            form.signature_file.data,
            filename=form.signature_file.data.filename,
            content_type=form.signature_file.data.content_type,
        )
    else:
        signature.file.replace(
            form.signature_file.data,
            filename=form.signature_file.data.filename,
            content_type=form.signature_file.data.content_type,
        )

    signature.last_updated_by = current_user._get_current_object()
    signature.updated_date = datetime.datetime.now()
    signature.ip_address = request.remote_addr
    signature.save()

    return redirect(url_for("users.profile", user_id=user_id))


@module.route("/change_organization/<organization_id>")
@login_required
def change_organization(organization_id):
    user = current_user._get_current_object()
    organization = models.Organization.objects.get(id=organization_id)
    if organization in user.organizations:
        user.user_setting.current_organization = organization
        user.user_setting.updated_date = datetime.datetime.now()
        user.save()

    return redirect(url_for("dashboard.index"))
