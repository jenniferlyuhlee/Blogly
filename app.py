"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def homepage():
    """Homepage that displays recents posts"""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('home.html', posts = posts)


@app.route('/users')
def list_users():
    """Shows list of all users in db"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('list.html', users = users)


@app.route('/users/new')
def show_form():
    """Shows form to submit new user"""
    return render_template('form.html')


@app.route('/users/new', methods = ["POST"])
def add_user():
    """Handles form submission to submit new user"""
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url']
    image_url = image_url if image_url else None
   
    new_user = User(first_name=first_name, 
                    last_name=last_name, 
                    image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details about clicked user"""
    user = User.query.get_or_404(user_id)
    posts = user.posts
    return render_template("details.html", 
                           user = user,
                           posts= posts)


@app.route('/users/<int:user_id>/edit')
def show_edit(user_id):
    """Show edit user page"""
    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user = user)


@app.route('/users/<int:user_id>/edit', methods = ["POST"])
def edit_user(user_id):
    """Handles editing user details"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first-name']
    user.last_name = request.form['last-name']
    user.image_url = request.form['image-url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods = ["POST"])
def delete_user(user_id):
    """Handles deleting user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new')
def add_post(user_id):
    """Shows add post form"""

    user = User.query.get_or_404(user_id)
    return render_template("post-form.html", user = user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def post_form(user_id):
    """Handles add post form"""
    
    title = request.form['title']
    content = request.form['content']
    new_post = Post(title=title, 
                    content=content,
                    user_id=user_id)
    
    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Shows post details"""
    post = Post.query.get_or_404(post_id)
    user = post.user
    return render_template("post-details.html", 
                           post = post,
                           user = user)


@app.route('/posts/<int:post_id>/edit')
def show_edit_post(post_id):
    """Shows edit post page"""
    post = Post.query.get_or_404(post_id)
    return render_template("edit-post.html", post = post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """Handles edit post form"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post.id}')


@app.route('/posts/<int:post_id>/delete', methods = ["POST"])
def delete_post(post_id):
    """Handles deleting post"""
    post = Post.query.get_or_404(post_id)
    user_id = post.user.id
    user = User.query.get_or_404(user_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')