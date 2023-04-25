from db import db


class FavoritePokemonModel(db.Model):
    __tablename__ = 'favorite_pokemons'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pokemon_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    types = db.Column(db.JSON(), nullable=False)
    image = db.Column(db.String(9999), nullable=False)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f"{self.id}"
