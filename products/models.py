from shop import db


class AddBook(db.Model):
    __seachbale__ = ['name', 'desc']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    desc = db.Column(db.String, nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'),nullable=False)
    genre = db.relationship('Genre', backref=db.backref('genre', lazy=True))
    image = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return '<Post %r>' % self.name


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        return '<Genre %r>' % self.name


db.create_all()