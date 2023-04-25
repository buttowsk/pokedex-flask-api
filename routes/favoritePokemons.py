from schemas.newFavoritePokemon import NewFavoritePokemonSchema
from schemas.favoritePokemon import FavoritePokemonSchema
from models.favoritePokemon import FavoritePokemonModel as FavoritePokemon
from flask import Blueprint, request, jsonify, make_response
from db import db
from utils import jwt_required_route

bp = Blueprint('favorite-pokemon-routes', __name__)


@bp.route('/users/<int:user_id>/favorites/pokemons', methods=['GET'])
@jwt_required_route
def get_all_fav_pokemons(user_id):
    get_favorite = FavoritePokemon.query.filter_by(user_id=user_id).all()
    favorite_schema = FavoritePokemonSchema(many=True)
    favorite = favorite_schema.dump(get_favorite)
    return make_response(jsonify({"favorite_pokemons": favorite}))


@bp.route('/users/<int:user_id>/favorites/pokemon/<int:pokemon_id>', methods=['GET'])
@jwt_required_route
def get_fav_pokemon_by_id(user_id, pokemon_id):
    get_favorite = FavoritePokemon.query.filter_by(user_id=user_id, pokemon_id=pokemon_id).first()
    favorite_schema = FavoritePokemonSchema()
    favorite = favorite_schema.dump(get_favorite)
    return make_response(jsonify({"favorite_pokemon": favorite}))


@bp.route('/users/<int:user_id>/favorites/pokemon/<int:pokemon_id>', methods=['DELETE'])
@jwt_required_route
def delete_fav_pokemon_by_id(user_id, pokemon_id):
    get_favorite = FavoritePokemon.query.filter_by(user_id=user_id, pokemon_id=pokemon_id).first()
    db.session.delete(get_favorite)
    db.session.commit()
    return make_response(jsonify({"favorite_pokemon_deleted": "Favorite deleted"}))


@bp.route('/users/<int:user_id>/favorites/pokemon', methods=['POST'])
@jwt_required_route
def add_favorite_pokemon(user_id):
    pokemon_id = request.json.get('pokemon_id', None)
    name = request.json.get('name', None)
    image = request.json.get('image', None)
    types = request.json.get('types', None)

    new_favorite_pokemon = FavoritePokemon(pokemon_id=pokemon_id, name=name, image=image, types=types, user_id=user_id)
    db.session.add(new_favorite_pokemon)
    db.session.commit()
    new_favorite_schema = NewFavoritePokemonSchema()
    new_favorite = new_favorite_schema.dump(new_favorite_pokemon)
    return make_response(jsonify({"favorite_pokemon": new_favorite})), 201
