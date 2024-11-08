from sql_alchemy import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    registered_by = db.Column(db.String, db.ForeignKey('user.email'), nullable=False)
    #reviews = db.relationship('Review', backref='book', lazy=True)

    @classmethod
    def book_exists(cls, title):
        return cls.query.filter_by(title=title).first()
    
    def save_book(self):
        db.session.add(self)
        db.session.commit()
    
    def update_book(self, title, description, gender, registered_by):
        self.title = title
        self.description = description
        self.gender = gender
        self.registered_by = registered_by
    
    def delete_book(self):
        db.session.delete(self)
        db.session.commit()  