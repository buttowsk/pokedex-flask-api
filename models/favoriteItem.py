from db import db


class FavoriteItemModel(db.Model):
    __tablename__ = 'favorite_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    item_name = db.Column(db.String(100), nullable=False)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, user_id, item_id, item_name):
        self.user_id = user_id
        self.item_id = item_id
        self.item_name = item_name

    def __repr__(self):
        return f"{self.id}"

