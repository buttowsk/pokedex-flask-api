from models.favoriteItem import FavoriteItemModel as FavoriteItem
from schemas.favoriteItem import FavoriteItemSchema
from schemas.newFavoriteItem import NewFavoriteItemSchema
from flask import Blueprint, request, jsonify, make_response
from db import db
from utils import jwt_required_route

bp = Blueprint('favorite-item-routes', __name__)


@bp.route('/users/<int:user_id>/favorites/item', methods=['GET'])
@jwt_required_route
def get_all_fav_items(user_id):
    get_favorite = FavoriteItem.query.filter_by(user_id=user_id).all()
    favorite_schema = FavoriteItemSchema(many=True)
    favorite = favorite_schema.dump(get_favorite)
    return make_response(jsonify({"favorite_items": favorite}))


@bp.route('/users/<int:user_id>/favorites/item/<int:item_id>', methods=['GET'])
@jwt_required_route
def get_fav_item_by_id(user_id, item_id):
    get_favorite = FavoriteItem.query.filter_by(user_id=user_id, item_id=item_id).first()
    favorite_schema = FavoriteItemSchema()
    favorite = favorite_schema.dump(get_favorite)
    return make_response(jsonify({"favorite_item": favorite}))


@bp.route('/users/<int:user_id>/favorites/item/<int:item_id>', methods=['DELETE'])
@jwt_required_route
def delete_fav_item_by_id(user_id, item_id):
    get_favorite = FavoriteItem.query.filter_by(user_id=user_id, item_id=item_id).first()
    db.session.delete(get_favorite)
    db.session.commit()
    return make_response(jsonify({"favorite_item_deleted": "Favorite deleted"}))


@bp.route('/users/<int:user_id>/favorites/item', methods=['POST'])
@jwt_required_route
def add_favorite_item(user_id):
    item_name = request.json.get('item_name', None)
    item_id = request.json.get('item_id', None)
    if not item_name:
        return jsonify({"msg": "Missing item_name parameter"}), 400
    if not item_id:
        return jsonify({"msg": "Missing item_id parameter"}), 400
    new_favorite_item = FavoriteItem(item_name=item_name, item_id=item_id, user_id=user_id)
    db.session.add(new_favorite_item)
    db.session.commit()
    new_favorite_schema = NewFavoriteItemSchema()
    new_favorite = new_favorite_schema.dump(new_favorite_item)
    return make_response(jsonify({"favorite_items_add": new_favorite}))
