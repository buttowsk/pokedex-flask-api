from db import db
from models.favoritePokemon import FavoritePokemonModel as FavoritePokemon
from models.favoriteItem import FavoriteItemModel as FavoriteItem


class UsersModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    favorite_pokemons = db.relationship(FavoritePokemon, backref='user', lazy=True)
    favorite_items = db.relationship(FavoriteItem, backref='user', lazy=True)

    @classmethod
    def create_from_google(cls, username, email):
        user = cls(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return user

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __int__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f"{self.id}"
