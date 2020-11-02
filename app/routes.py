from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_required
from app import app, db
from app.forms import PostForm
from app.models import User, Post
from app.uploads.forms import UploadFileForm

@app.route('/')
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    if current_user.is_authenticated:
        form = PostForm()
        return render_template('index.html', form=form, posts=posts)
    return render_template('index.html', posts=posts)


@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.created_at.desc())
    if user == current_user:
        form = UploadFileForm()
        return render_template('user.html', user=user, form=form, posts=posts)
    return render_template('user.html', user=user, posts=posts)


@app.route('/upload_post', methods=['POST'])
@login_required
def upload_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(u'Your post is live!', 'success')
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))