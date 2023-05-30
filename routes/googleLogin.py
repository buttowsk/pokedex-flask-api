import os
from flask import redirect, url_for, Blueprint
from flask_dance.contrib.google import make_google_blueprint, google
from dotenv import load_dotenv
import logging
from db import db
from flask_jwt_extended import create_access_token
from models.users import UsersModel

load_dotenv()

client_id = os.getenv("GOOGLE_CLIENT_ID")
client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

bp = Blueprint('google_routes', __name__)

google_auth_bp = make_google_blueprint(
    client_id=client_id,
    client_secret=client_secret,
    reprompt_consent=True,
    scope=["profile", "email"],
    redirect_url='/google/authorized'
)


@bp.route("/login/google")
def login():
    if not google.authorized:
        return redirect(url_for("google.login"))

    return redirect(url_for("google.authorized"))


@bp.route("/google/authorized")
def authorized():
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v1/userinfo")
    user_info = resp.json()

    user = UsersModel.query.filter_by(email=user_info["email"]).first()
    if not user:
        user = UsersModel(username=user_info["name"], email=user_info["email"])
        db.session.add(user)
        db.session.commit()

    access_token = create_access_token(identity=user.id)

    # Redirecionar o usuário para o front-end com o token de acesso
    frontend_url = "https://buttowsk.github.io/pokedex-react/#/?token=" + access_token
    return redirect(frontend_url)


@bp.route("/logout/google")
def logout():
    token = google.token["access_token"]
    google.post(
        "https://accounts.google.com/o/oauth2/revoke",
        params={"token": token},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    # Aqui você pode redirecionar o usuário para o front-end
    frontend_url = "http://localhost:5173/pokedex-react/"
    return redirect(frontend_url)
