import datetime
from flask import Blueprint, request, jsonify, make_response, redirect
from flask_jwt_extended import get_jwt_identity, create_access_token
from models.users import UsersModel as Users
from schemas.users import UserSchema
from db import db
from utils import jwt_required_route


bp = Blueprint('user-routes', __name__)

@bp.route('/users', methods=['GET'])
def get_all_users():
    get_users = Users.query.all()
    user_schema = UserSchema(many=True)
    users = user_schema.dump(get_users)
    return make_response(jsonify({"users": users}))


@bp.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)
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

    new_user = Users(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201


@bp.route('/login', methods=['POST'])
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

@bp.route('/logout', methods=['POST'])
@jwt_required_route
def logout():
    return jsonify({"msg": "Successfully logged out"}), 200


@bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required_route
def get_user_by_id(user_id):
    get_user = Users.query.get_or_404(user_id)
    user_schema = UserSchema()
    user = user_schema.dump(get_user)
    return make_response(jsonify({"user": user}))


@bp.route('/check-token', methods=['GET'])
@jwt_required_route
def check_token():
    return jsonify('Token is valid!'), 200


@bp.route('/get-user-id', methods=['GET'])
@jwt_required_route
def get_user_id():
    current_user = get_jwt_identity()
    return jsonify(user_id=current_user), 200


@bp.route('/get-name', methods=['GET'])
@jwt_required_route
def get_name():
    current_user = get_jwt_identity()
    user = Users.query.get_or_404(current_user)
    return jsonify(name=user.username), 200


@bp.route('/delete-user', methods=['DELETE'])
@jwt_required_route
def delete_user():
    current_user = get_jwt_identity()
    user = Users.query.get_or_404(current_user)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User deleted successfully"}), 200
