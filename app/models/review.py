from sql_alchemy import db
from datetime import datetime, timezone

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500))
    user_email = db.Column(db.String(80), db.ForeignKey('user.email'), nullable=False)
    book_title = db.Column(db.String(100), db.ForeignKey('book.title'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    @classmethod
    def review_exists(cls, id):
        return cls.query.filter_by(id=id).fisrt()
    
    def save_review(self):
        db.session.add(self)
        db.session.commit()
    
    def update_review(self, rating, comment, user_email, book_title):
        self.rating = rating
        self.comment = comment
        self.user_email = user_email
        self.book_title = book_title

    def delete_review(self):
        db.session.delete(self)
        db.session.commit()