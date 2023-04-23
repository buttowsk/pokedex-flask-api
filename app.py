import datetime
from functools import wraps
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "super-secret-123"  # Change this!
jwt = JWTManager(app)
app.app_context().push()
db = SQLAlchemy(app)


def jwt_required_route(route):
    @wraps(route)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        return route(*args, **kwargs)

    return wrapper


class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pokemon_name = db.Column(db.String(100))
    pokemon_id = db.Column(db.Integer)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __int__(self, user_id, pokemon_name, pokemon_id):
        self.user_id = user_id
        self.pokemon_name = pokemon_name
        self.pokemon_id = pokemon_id

    def __repr__(self):
        return f"{self.id}"


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    favorites = db.relationship('Favorites', backref='user', lazy=True)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __int__(self, fullname, username, email, password):
        self.fullname = fullname
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f"{self.id}"


db.create_all()


class FavoritesSchema(Schema):
    class Meta(Schema.Meta):
        model = Favorites
        sqla_session = db.session
        load_instance = True
        include_relationships = True
        fields = ('id', 'user_id', 'pokemon_name', 'pokemon_id')


class NewFavoriteSchema(Schema):
    class Meta(Schema.Meta):
        model = Favorites
        sqla_session = db.session
        fields = ('id', 'user_id', 'pokemon_name', 'pokemon_id')


class UserSchema(Schema):
    class Meta:
        model = Users
        sqla_session = db.session
        include_relationships = True
        load_instance = True

    id = fields.Int(dump_only=True)
    fullname = fields.Str(required=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    favorites = fields.Nested('FavoritesSchema', many=True)


@app.route('/users', methods=['GET'])
def get_all_users():
    get_users = Users.query.all()
    user_schema = UserSchema(many=True)
    users = user_schema.dump(get_users)
    return make_response(jsonify({"users": users}))


@app.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    fullname = request.json.get('fullname', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not fullname:
        return jsonify({"msg": "Missing name parameter"}), 400
    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    email_exists = Users.query.filter_by(email=email).first()
    if email_exists:
        return jsonify({"msg": "Email already exists"}), 400
    username_exists = Users.query.filter_by(username=username).first()
    if username_exists:
        return jsonify({"msg": "Username already exists"}), 400

    new_user = Users(username=username, fullname=fullname, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    user = Users.query.filter_by(email=email).first()
    if not user:
        return jsonify({"msg": "Bad email or password"}), 401

    if user.password != password:
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(hours=1))
    return jsonify(access_token=access_token), 200


@app.route('/logout', methods=['POST'])
@jwt_required_route
def logout():
    return jsonify({"msg": "Successfully logged out"}), 200


@app.route('/check-token', methods=['GET'])
@jwt_required_route
def check_token():
    return jsonify('Token is valid!'), 200


@app.route('/get-user-id', methods=['GET'])
@jwt_required_route
def get_user_id():
    current_user = get_jwt_identity()
    return jsonify(user_id=current_user), 200


@app.route('/get-name', methods=['GET'])
@jwt_required_route
def get_name():
    current_user = get_jwt_identity()
    user = Users.query.get_or_404(current_user)
    return jsonify(name=user.username), 200


@app.route('/users/<int:user_id>', methods=['GET'])
@jwt_required_route
def get_user_by_id(user_id):
    get_user = Users.query.get_or_404(user_id)
    user_schema = UserSchema()
    user = user_schema.dump(get_user)
    return make_response(jsonify({"user": user}))


@app.route('/users/<int:user_id>/favorites', methods=['GET'])
@jwt_required_route
def get_user_favorites(user_id):
    get_user = Users.query.get_or_404(user_id)
    favorites_schema = FavoritesSchema(many=True)
    favorites = favorites_schema.dump(get_user.favorites)
    return make_response(jsonify({"favorites": favorites}))


@app.route('/users/<int:user_id>/favorites/<int:pokemon_id>', methods=['GET'])
@jwt_required_route
def get_user_favorites_by_pokemon_id(user_id, pokemon_id):
    get_user = Users.query.get_or_404(user_id)
    get_favorite = Favorites.query.filter_by(user_id=user_id, pokemon_id=pokemon_id).first()
    favorites_schema = FavoritesSchema()
    favorite = favorites_schema.dump(get_favorite)
    return make_response(jsonify({"favorite": favorite}))


@app.route('/users/<int:user_id>/favorites/<int:pokemon_id>', methods=['DELETE'])
@jwt_required_route
def delete_user_favorites_by_pokemon_id(user_id, pokemon_id):
    get_user = Users.query.get_or_404(user_id)
    get_favorite = Favorites.query.filter_by(user_id=user_id, pokemon_id=pokemon_id).first()
    db.session.delete(get_favorite)
    db.session.commit()
    return make_response(jsonify({"favorite": "Favorite deleted"}))


@app.route('/users/<int:user_id>/favorites', methods=['POST'])
@jwt_required_route
def add_user_favorites(user_id):
    get_user = Users.query.get_or_404(user_id)
    pokemon_name = request.json.get('pokemon_name', None)
    pokemon_id = request.json.get('pokemon_id', None)
    if not pokemon_name:
        return jsonify({"msg": "Missing name parameter"}), 400
    new_favorite = Favorites(user_id=user_id, pokemon_name=pokemon_name, pokemon_id=pokemon_id)
    db.session.add(new_favorite)
    db.session.commit()
    new_favorite_schema = NewFavoriteSchema()
    favorite = new_favorite_schema.dump(new_favorite)
    return make_response(jsonify({"favorite": favorite}))


if __name__ == '__main__':
    app.run()
