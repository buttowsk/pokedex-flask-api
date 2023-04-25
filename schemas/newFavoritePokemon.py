from ma import ma
from models.favoritePokemon import FavoritePokemonModel
from db import db


class NewFavoritePokemonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FavoritePokemonModel
        sqla_session = db.session

    user_id = ma.Int(required=True)
    pokemon_id = ma.Int(required=True)
    name = ma.Str(required=True)
    image = ma.Str(required=True)
    types = ma.Str(required=True)
