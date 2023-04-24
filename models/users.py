from db import db
from models.favoritePokemon import FavoritePokemonModel as FavoritePokemon
from models.favoriteItem import FavoriteItemModel as FavoriteItem


class UsersModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    favorite_pokemons = db.relationship(FavoritePokemon, backref='user', lazy=True)
    favorite_items = db.relationship(FavoriteItem, backref='user', lazy=True)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __int__(self, fullname, username, email, password):
        self.fullname = fullname
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f"{self.id}"
