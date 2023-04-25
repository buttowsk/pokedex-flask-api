from db import db


class FavoriteItemModel(db.Model):
    __tablename__ = 'favorite_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(9999), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(9999), nullable=False)
    held_by_pokemon = db.Column(db.String(9999), nullable=False)
    category = db.Column(db.String(9999), nullable=False)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f"{self.id}"
