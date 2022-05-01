"""Blogly application."""

from flask import Flask, redirect, render_template, request
from models import db, connect_db, User, Post, PostTag, Tag
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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404_page.html')


@app.route('/users')
def user_home():
    '''Display a full list of users'''

    users = User.query.all()

    return render_template("/user/index.html", users= users)


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
        return render_template('/user/new_user.html')


@app.route('/users/<user_id>')
def user_profile(user_id):
    '''Display user profile'''

    user = User.query.get_or_404(user_id)
    post_list = Post.query.filter(Post.user_id == user_id).all()
    prof_pic = user.image_url

    return render_template('/user/user_profile.html', pic=prof_pic, name=user.full_name, id=user_id, posts= post_list)


@app.route('/users/<user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    '''Render edit user screen and post changes to database'''

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
        return render_template('/user/edit_user.html', id= user_id, fname = first_name, lname = last_name, pic= prof_pic)


@app.route('/users/<user_id>/delete', methods=['GET', 'POST'])
def delete_user(user_id):
    '''Delete user'''

    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()

        return redirect('/users')

    else:
        return render_template('/user/user_delete.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['GET', 'POST'])
def render_newpost_form(user_id):
    '''Render form for new post or post it to db if method == POST'''

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['post_content']
        tags = request.form.getlist('tags')

        post = Post(title=title, content=content, user_id= user.id)
        db.session.add(post)
        db.session.commit()

        for tag in tags:
            add_tag = PostTag(post_id=post.id, tag_id=tag)
            db.session.add(add_tag)
        db.session.commit()

        return redirect(f"/users/{user.id}")

    else:
        return render_template('/posts/create_post.html', user=user, tags=tags)


@app.route('/posts/<int:post_id>')
def post_page(post_id):

    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)

    return render_template('/posts/view_post.html', post=post, user=user)


@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_posts(post_id):
    '''Render post edit form and post to database if method == POST'''

    post = Post.query.get_or_404(post_id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['post_content']

        db.session.add(post)
        db.session.commit()

        return redirect(f"/users/{post.user_id}")

    else:
        return render_template('/posts/edit_post.html', post=post)


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    '''Select post and delete from database'''
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")


@app.route('/tags')
def list_tags():
    '''Display the list of tags'''

    tags = Tag.query.all()

    return render_template('/tags/tags_list.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def view_tag(tag_id):
    '''View individual tag information'''

    tag = Tag.query.get_or_404(tag_id)

    return render_template('/tags/tag_info.html', tag= tag)


@app.route('/tags/new', methods=['GET', 'POST'])
def create_tag():
    '''Display form to create new tag in database'''

    if request.method == 'POST':
        tag_name = request.form['name']
        tag = Tag(name=tag_name)
        db.session.add(tag)
        db.session.commit()

        return redirect('/tags')

    else:
        return render_template('/tags/create_tag.html')


@app.route('/tags/<int:tag_id>/edit', methods=['GET', 'POST'])
def edit_tag(tag_id):
    '''Navigate to tag info and edit'''

    tag = Tag.query.get(tag_id)

    if request.method == 'POST':
        tag.name = request.form['name']
        db.session.add(tag)
        db.session.commit()

        return redirect('/tags')

    else:
        return render_template('/tags/edit_tag.html', tag=tag)


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    '''Delete tag from database'''

    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')
