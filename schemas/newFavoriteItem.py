from ma import ma
from models.favoriteItem import FavoriteItemModel
from db import db


class NewFavoriteItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FavoriteItemModel
        sqla_session = db.session
        fields = ('user_id', 'item_id', 'item_name')

    user_id = ma.Int(required=True)
    item_id = ma.Int(required=True)
    item_name = ma.Str(required=True)
