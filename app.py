import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from db import init_db_app
from ma import init_ma_app
from routes.user import bp as user_routes
from routes.favoriteItems import bp as favorites_routes
from routes.favoritePokemons import bp as favorite_pokemons_routes
from routes.googleLogin import google_auth_bp, bp as google_routes
import logging

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")
app.secret_key = os.getenv("SECRET_KEY")

CORS(app)
jwt = JWTManager(app)

app.register_blueprint(user_routes)
app.register_blueprint(favorites_routes)
app.register_blueprint(favorite_pokemons_routes)
app.register_blueprint(google_auth_bp, url_prefix="/login")
app.register_blueprint(google_routes)

init_db_app(app)
init_ma_app(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
