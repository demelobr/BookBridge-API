from sql_alchemy import db
import re

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    # reviews = ... Teremos o registro de todas as reviews feitas por aquele user

    @classmethod
    def user_exists(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def is_valid_email(cls, email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email)

    def save_user(self):
        db.session.add(self)
        db.session.commit()
    
    def update_user(self, email, password):
        self.email = email
        self.password = password

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()    