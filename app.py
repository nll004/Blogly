"""Blogly application."""

from flask import Flask, redirect, render_template, request
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'ahaeithet'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def redirect_to_main():
    '''Redirect to main user page'''
    return redirect('/users')


@app.route('/users')
def user_home():
    '''Display a full list of users'''

    users = User.query.all()

    return render_template("user_home.html", users= users)


@app.route('/users/new', methods=['GET', 'POST'])
def create_new_user():
    '''Load form for new user and post submitted user info to database'''

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        prof_pic = request.form['picture']
        if not prof_pic:
            prof_pic = None

        user = User(first_name=first_name, last_name=last_name, image_url=prof_pic)

        db.session.add(user)
        db.session.commit()

        return redirect('/users')

    else:
        return render_template('new_user.html')


@app.route('/users/<user_id>')
def user_profile(user_id):
    '''Display user profile'''

    user = User.query.get_or_404(user_id)
    prof_pic = user.image_url

    return render_template('profile.html', pic=prof_pic, name=user.full_name, id=user_id)


@app.route('/users/<user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):

    user = User.query.get_or_404(user_id)
    first_name = user.first_name
    last_name = user.last_name
    prof_pic = user.image_url

    if request.method == "POST":
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form['picture']
        if not user.image_url:
            user.image_url = None
        db.session.add(user)
        db.session.commit()

        return redirect('/users')

    else:
        return render_template('edit_user.html', id= user_id, fname = first_name, lname = last_name, pic= prof_pic)


@app.route('/users/<user_id>/delete', methods=['GET', 'POST'])
def delete_user(user_id):
    '''Delete user'''

    user = user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()

        return redirect('/users')

    else:
        return render_template('user_delete.html', user=user)
