from flask import Blueprint, request, redirect, url_for, render_template
from flask_blogly.models import db, User, Post, Tag, PostTag

main_bp = Blueprint('main', __name__)

# User Routes
@main_bp.route('/users')
def list_users():
    users = User.query.all()
    return render_template('users/index.html', users=users)

@main_bp.route('/users/<int:id>')
def show_user(id):
    user = User.query.get_or_404(id)
    return render_template('users/show.html', user=user)

@main_bp.route('/users/new', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        new_user = User(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            image_url=request.form['image_url']
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main.list_users'))
    return render_template('users/new.html')

@main_bp.route('/users/<int:id>/edit', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form['image_url']
        db.session.commit()
        return redirect(url_for('main.show_user', id=user.id))
    return render_template('users/edit.html', user=user)

@main_bp.route('/users/<int:id>/delete', methods=['POST'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('main.list_users'))

# Post Routes
@main_bp.route('/posts')
def list_posts():
    posts = Post.query.all()
    return render_template('posts/index.html', posts=posts)

@main_bp.route('/posts/<int:id>')
def show_post(id):
    post = Post.query.get_or_404(id)
    return render_template('posts/show.html', post=post)

@main_bp.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        tags = request.form.getlist('tags')
        new_post = Post(
            title=request.form['title'],
            content=request.form['content'],
            user_id=request.form['user_id']
        )
        db.session.add(new_post)
        for tag_id in tags:
            tag = Tag.query.get(tag_id)
            if tag:
                new_post.tags.append(tag)
        db.session.commit()
        return redirect(url_for('main.list_posts'))
    tags = Tag.query.all()
    return render_template('posts/new.html', tags=tags)

@main_bp.route('/posts/<int:id>/edit', methods=['GET', 'POST'])
def edit_post(id):
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        tags = request.form.getlist('tags')
        post.tags = []
        for tag_id in tags:
            tag = Tag.query.get(tag_id)
            if tag:
                post.tags.append(tag)
        db.session.commit()
        return redirect(url_for('main.show_post', id=post.id))
    tags = Tag.query.all()
    return render_template('posts/edit.html', post=post, tags=tags)

@main_bp.route('/posts/<int:id>/delete', methods=['POST'])
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main.list_posts'))

# Tag Routes
@main_bp.route('/tags')
def list_tags():
    tags = Tag.query.all()
    return render_template('tags/index.html', tags=tags)

@main_bp.route('/tags/<int:id>')
def show_tag(id):
    tag = Tag.query.get_or_404(id)
    return render_template('tags/show.html', tag=tag)

@main_bp.route('/tags/new', methods=['GET', 'POST'])
def new_tag():
    if request.method == 'POST':
        new_tag = Tag(name=request.form['name'])
        db.session.add(new_tag)
        db.session.commit()
        return redirect(url_for('main.list_tags'))
    return render_template('tags/new.html')

@main_bp.route('/tags/<int:id>/edit', methods=['GET', 'POST'])
def edit_tag(id):
    tag = Tag.query.get_or_404(id)
    if request.method == 'POST':
        tag.name = request.form['name']
        db.session.commit()
        return redirect(url_for('main.show_tag', id=tag.id))
    return render_template('tags/edit.html', tag=tag)

@main_bp.route('/tags/<int:id>/delete', methods=['POST'])
def delete_tag(id):
    tag = Tag.query.get_or_404(id)
    db.session.delete(tag)
    db.session.commit()
    return redirect(url_for('main.list_tags'))