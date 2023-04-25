from ma import ma
from models.favoriteItem import FavoriteItemModel
from db import db


class NewFavoriteItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FavoriteItemModel
        sqla_session = db.session

    user_id = ma.Int(required=True)
    item_id = ma.Int(required=True)
    name = ma.Str(required=True)
    image = ma.Str(required=True)
    cost = ma.Int(required=True)
    description = ma.Str(required=True)
    held_by_pokemon = ma.Str(required=True)
    category = ma.Str(required=True)

