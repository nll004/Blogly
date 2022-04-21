"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    '''Connect to database'''

    db.app = app
    db.init_app(app)

class User(db.Model):
    '''User class template'''

    __tablename__ = 'user'

    def __repr__(self):
        return f"User: {self.first_name} {self.last_name}. Picture URL: {self.image_url}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)
    image_url = db.Column(db.Text,
                default = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg')
