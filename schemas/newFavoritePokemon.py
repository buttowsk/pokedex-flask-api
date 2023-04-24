from ma import ma
from models.favoritePokemon import FavoritePokemonModel
from db import db


class NewFavoritePokemonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FavoritePokemonModel
        sqla_session = db.session
        fields = ('user_id', 'pokemon_id', 'pokemon_name')

    user_id = ma.Int(required=True)
    pokemon_id = ma.Int(required=True)
    pokemon_name = ma.Str(required=True)
