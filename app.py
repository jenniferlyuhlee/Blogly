"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

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

###############################---USERS---#############################
@app.route('/users')
def list_users():
    """Shows list of all users in db"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('user/list.html', users = users)


@app.route('/users/new')
def show_form():
    """Shows form to submit new user"""
    return render_template('user/form.html')


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
    
    flash(f"User {new_user.full_name} added!", "success")
    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details about clicked user"""
    user = User.query.get_or_404(user_id)
    posts = user.posts
    return render_template("user/details.html", 
                           user = user,
                           posts= posts)


@app.route('/users/<int:user_id>/edit')
def show_edit(user_id):
    """Show edit user page"""
    user = User.query.get_or_404(user_id)
    return render_template("user/edit.html", user = user)


@app.route('/users/<int:user_id>/edit', methods = ["POST"])
def edit_user(user_id):
    """Handles editing user details"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first-name']
    user.last_name = request.form['last-name']
    user.image_url = request.form['image-url']

    db.session.add(user)
    db.session.commit()

    flash(f"User {user.full_name} edited!", "success")
    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods = ["POST"])
def delete_user(user_id):
    """Handles deleting user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    flash(f"User {user.full_name} deleted!", "danger")
    return redirect('/users')

###############################---POSTS---#############################
@app.route('/users/<int:user_id>/posts/new')
def post_form(user_id):
    """Shows add post form"""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.order_by(Tag.name).all()
    return render_template("post/post-form.html", 
                           user = user,
                           tags = tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    """Handles add post form"""
    
    title = request.form['title']
    content = request.form['content']
    new_post = Post(title=title, 
                    content=content,
                    user_id=user_id)
    
    tag_ids = [int(id) for id in request.form.getlist('tags')]
    for tag_id in tag_ids:
        new_post.tags.append(Tag.query.get_or_404(tag_id))
    
    db.session.add(new_post)
    db.session.commit()

    flash(f"Posted!", "success")
    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Shows post details"""
    post = Post.query.get_or_404(post_id)
    user = post.user
    return render_template("post/post-details.html", 
                           post = post,
                           user = user)


@app.route('/posts/<int:post_id>/edit')
def show_edit_post(post_id):
    """Shows edit post page"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.order_by(Tag.name).all()
    return render_template("post/edit-post.html", 
                           post = post,
                           tags = tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """Handles edit post form"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(id) for id in request.form.getlist('tags')]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    flash(f"Post edited!", "success")
    return redirect(f'/posts/{post.id}')


@app.route('/posts/<int:post_id>/delete', methods = ["POST"])
def delete_post(post_id):
    """Handles deleting post"""
    post = Post.query.get_or_404(post_id)
    user_id = post.user.id
    user = User.query.get_or_404(user_id)

    db.session.delete(post)
    db.session.commit()

    flash(f"Post deleted!", "danger")
    return redirect(f'/users/{user_id}')

###############################---TAGS---#############################
@app.route('/tags')
def list_tags():
    """Shows list of all tags in db"""
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('tag/tag-list.html', tags = tags)


@app.route('/tags/<int:tag_id>')
def show_tag_posts(tag_id):
    """Shows posts under tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag/tag-posts.html', tag=tag)


@app.route('/tags/new')
def tag_form():
    """Shows form to add tag"""
    
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('tag/tag-form.html', posts=posts)


@app.route('/tags/new', methods = ["POST"])
def add_tag():
    """Handles add tag form"""
    
    try:
        name = request.form['name']
        new_tag = Tag(name=name)

        post_ids = [int(id) for id in request.form.getlist('posts')]
        for post_id in post_ids:
            new_tag.posts.append(Post.query.get_or_404(post_id))
        
        db.session.add(new_tag)
        db.session.commit()
        flash(f"Tag {new_tag.name} added!", "success")

    except:
        flash("Tag already exists! Please enter a new tag.", "danger")

    return redirect(f'/tags')

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag(tag_id):
    """Shows edit tag page"""
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.order_by(Post.created_at.desc()).all()

    return render_template("tag/edit-tag.html", 
                           tag = tag,
                           posts = posts)


@app.route('/tags/<int:tag_id>/edit', methods = ["POST"])
def edit_tag(tag_id):
    """Handles editing tag"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']

    post_ids = [int(id) for id in request.form.getlist('posts')]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    flash(f"Tag {tag.name} edited!", "success")
    return redirect(f'/tags')


@app.route('/tags/<int:tag_id>/delete', methods = ["POST"])
def delete_tag(tag_id):
    """Handles deleting tag"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    flash(f"Tag {tag.name} deleted!", "danger")
    return redirect(f'/tags')