from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

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
