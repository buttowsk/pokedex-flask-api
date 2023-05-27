from ma import ma
from models.users import UsersModel
from db import db
from schemas.favoritePokemon import FavoritePokemonSchema
from schemas.favoriteItem import FavoriteItemSchema


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UsersModel
        sqla_session = db.session
        include_relationships = True
        load_instance = True

    id = ma.Int(dump_only=True)
    username = ma.Str(required=True)
    email = ma.Str(required=True)
    password = ma.Str(required=True)
    favorite_pokemons = ma.Nested(FavoritePokemonSchema, many=True)
    favorite_items = ma.Nested(FavoriteItemSchema, many=True)
