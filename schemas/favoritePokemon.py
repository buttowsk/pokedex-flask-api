from models.favoritePokemon import FavoritePokemonModel
from db import db
from ma import ma


class FavoritePokemonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FavoritePokemonModel
        sqla_session = db.session
        include_relationships = True
        load_instance = True

    id = ma.Int(dump_only=True)
    user_id = ma.Int(required=True)
    pokemon_id = ma.Int(required=True)
    pokemon_name = ma.Str(required=True)
