"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    '''Connect to database'''

    db.app = app
    db.init_app(app)

class User(db.Model):
    '''User class template'''

    __tablename__ = 'users'

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)
    image_url = db.Column(db.Text,
                default = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg')


class Post(db.Model):
    '''Post template model for database'''

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(30), nullable= False)
    content = db.Column(db.Text, nullable= False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable= False)
