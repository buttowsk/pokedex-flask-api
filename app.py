from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from db import init_db_app
from ma import init_ma_app
from routes.user import bp as user_routes
from routes.favoriteItems import bp as favorites_routes
from routes.favoritePokemons import bp as favorite_pokemons_routes

app = Flask(__name__)
CORS(app)
app.register_blueprint(user_routes)
app.register_blueprint(favorites_routes)
app.register_blueprint(favorite_pokemons_routes)
jwt = JWTManager(app)
app.app_context().push()
init_db_app(app)
init_ma_app(app)

if __name__ == '__main__':
    app.run()
