from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for
from pydantic import ValidationError

from src.api_v1.posts import api
from src.auth import login_required
from src.api_v1.posts.models import PostBody


blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/')
@login_required
def index():
    posts = api.get_posts()
    if post is None:
        abort(404)
    return render_template('index.html', posts=posts)

@blog_bp.route('/<int:id>')
@login_required
def post(id):
    post = api.get_posts(id)
    if post is None:
        abort(404)
    return render_template('post.html', post=post)

@blog_bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        try:
            title = request.form['title']
            content = request.form['content']
            post = PostBody(title=title, content=content)
            api.create(post)
            return redirect(url_for('index'))
        except ValidationError as err:
            flash(err)
    return render_template('create.html')

@blog_bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    post = api.get_posts(id)
    if post is None:
        abort(404)
    if request.method == 'POST':
        try:
            title = request.form['title']
            content = request.form['content']
            post_update = PostBody(title=title, content=content)
            api.update(post, post_update, partial=True)
            return redirect(url_for('index'))
        except ValidationError as err:
            flash(err)
    return render_template('edit.html', post=post)

@blog_bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = api.get_posts(id)
    if post is None:
        abort(404)
    api.delete(post)
    flash(f"'{post.title}' was successfully deleted!")
    return redirect(url_for('index'))

@blog_bp.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('auth.login'))