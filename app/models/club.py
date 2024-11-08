from sql_alchemy import db

# Tabela de associação para a relação muitos-para-muitos entre Club e Book
club_book = db.Table('club_book',
    db.Column('club_id', db.Integer, db.ForeignKey('club.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True)
)

class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    books = db.relationship('Book', secondary=club_book, backref=db.backref('clubs', lazy='dynamic'))
    
    @classmethod
    def club_exists(cls, name):
        return cls.query.filter_by(name=name).first()
    
    def save_club(self):
        db.session.add(self)
        db.session.commit()
    
    def update_club(self, name, owner_id):
        self.name = name
        self.owner_id = owner_id

    def delete_club(self):
        db.session.delete(self)
        db.session.commit()  