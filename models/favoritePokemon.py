from db import db


class FavoritePokemonModel(db.Model):
    __tablename__ = 'favorite_pokemons'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pokemon_id = db.Column(db.Integer, nullable=False)
    pokemon_name = db.Column(db.String(100), nullable=False)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, user_id, pokemon_id, pokemon_name):
        self.user_id = user_id
        self.pokemon_id = pokemon_id
        self.pokemon_name = pokemon_name

    def __repr__(self):
        return f"{self.id}"
