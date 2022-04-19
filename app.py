"""Blogly application."""

from flask import Flask, render_template
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.route('/')
def home_page():
    '''Display home'''

    users = User.query.all()

    return render_template("home.html", users= users)

@app.route('/new_user')
def new_user_page():
    '''Display new user page and form'''

    return render_template('new_user.html')

@app.route('/sav-user')
def save_new_user():
    '''Post new user info to database'''
