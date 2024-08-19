from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecret'

toolbar = DebugToolbarExtension(app)
connect_db(app)

# Create tables within an application context
with app.app_context():
    db.create_all()

@app.route('/')
def homepage():
    """Redirect to the list of users."""
    return redirect("/users")

##############################################################################
# User routes

@app.route('/users')
def list_users():
    """Display a page with information about all users."""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=["GET"])
def new_user_form():
    """Display the form to create a new user."""
    return render_template('users/new.html')

@app.route("/users/new", methods=["POST"])
def create_user():
    """Handle the submission for creating a new user."""
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        profile_picture=request.form['profile_picture'] or None
    )
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Display a page with information about a specific user."""
    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["GET"])
def edit_user_form(user_id):
    """Display the form to edit an existing user."""
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    """Handle the submission for updating an existing user."""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.profile_picture = request.form['profile_picture']
    db.session.commit()
    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Handle the deletion of an existing user."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")

##############################################################################
# Post routes

@app.route('/users/<int:user_id>/posts/new', methods=["GET", "POST"])
def add_post(user_id):
    """Handle form submission and add a new post for the user."""
    user = User.query.get_or_404(user_id)
    
    if request.method == "POST":
        new_post = Post(
            title=request.form['title'],
            content=request.form['content'],
            user_id=user.id
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(f"/users/{user.id}")
    
    return render_template('posts/new.html', user=user)

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Display a single post."""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["GET", "POST"])
def edit_post(post_id):
    """Handle editing an existing post."""
    post = Post.query.get_or_404(post_id)
    
    if request.method == "POST":
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(f"/users/{post.user_id}")
    
    return render_template('posts/edit.html', post=post)

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Handle deleting a post."""
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{user_id}")
