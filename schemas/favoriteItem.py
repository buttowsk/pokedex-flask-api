from models.favoriteItem import FavoriteItemModel
from db import db
from ma import ma


class FavoriteItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FavoriteItemModel
        sqla_session = db.session
        include_relationships = True
        load_instance = True

    id = ma.Int(dump_only=True)
    user_id = ma.Int(required=True)
    item_id = ma.Int(required=True)
    name = ma.Str(required=True)
    image = ma.Str(required=True)
    cost = ma.Int(required=True)
    description = ma.Str(required=True)
    held_by_pokemon = ma.Str(required=False)
    category = ma.Str(required=True)

