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
    item_name = ma.Str(required=True)
