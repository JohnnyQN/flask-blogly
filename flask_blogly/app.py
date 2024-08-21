from flask import Flask, render_template, request, redirect, flash
from flask_blogly.models import db, User, Post, Tag, PostTag
from flask_migrate import Migrate

import os
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql:///your_default_db')


app = Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Print available templates
print(app.jinja_env.loader.list_templates())

@app.route('/')
def root():
    """Show recent list of posts, most-recent first."""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("posts/homepage.html", posts=posts)

# Tag routes
@app.route('/tags')
def list_tags():
    """Display all tags."""
    tags = Tag.query.all()
    return render_template('tags/index.html', tags=tags)

@app.route('/tags/new', methods=["GET", "POST"])
def create_tag():
    """Create a new tag."""
    if request.method == "POST":
        tag_name = request.form['name']
        if Tag.query.filter_by(name=tag_name).first():
            flash("Tag already exists!")
            return redirect('/tags/new')
        tag = Tag(name=tag_name)
        db.session.add(tag)
        db.session.commit()
        flash(f"Tag '{tag.name}' added.")
        return redirect('/tags')
    return render_template('tags/new.html')

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """Display details of a specific tag."""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/show.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["GET", "POST"])
def edit_tag(tag_id):
    """Edit an existing tag."""
    tag = Tag.query.get_or_404(tag_id)
    if request.method == "POST":
        tag.name = request.form['name']
        db.session.commit()
        flash(f"Tag '{tag.name}' updated.")
        return redirect('/tags')
    return render_template('tags/edit.html', tag=tag)

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Delete a tag."""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' deleted.")
    return redirect('/tags')

# Post routes
@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Display a specific post with its tags."""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["GET", "POST"])
def edit_post(post_id):
    """Edit a post and its tags."""
    post = Post.query.get_or_404(post_id)
    if request.method == "POST":
        post.title = request.form['title']
        post.content = request.form['content']
        tag_ids = request.form.getlist('tags')
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        post.tags = tags
        db.session.commit()
        flash(f"Post '{post.title}' updated.")
        return redirect(f"/posts/{post.id}")
    tags = Tag.query.all()
    return render_template('posts/edit.html', post=post, tags=tags)

# User post routes
@app.route('/users/<int:user_id>/posts/new', methods=["GET", "POST"])
def create_post(user_id):
    """Create a new post with tags."""
    user = User.query.get_or_404(user_id)
    if request.method == "POST":
        post = Post(
            title=request.form['title'],
            content=request.form['content'],
            user=user
        )
        tag_ids = request.form.getlist('tags')
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        post.tags = tags
        db.session.add(post)
        db.session.commit()
        flash(f"Post '{post.title}' added.")
        return redirect(f"/users/{user.id}")
    tags = Tag.query.all()
    return render_template('posts/new.html', user=user, tags=tags)

if __name__ == '__main__':
    app.run(debug=True)
