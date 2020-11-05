from spotifytools import db


class Genre(db.Model):
    name = db.Column(db.String, primary_key=True)
    description = db.Column(db.String)
    sub_genres = db.relationship('Genre', backref='super_genre', lazy=True)
    wiki_url = db.Column(db.String)

    def __repr__(self) -> str:
        return f"Genre('{self.name}', '{self.wiki_url}'"
