from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_required
from app import app, db
from app.forms import PostForm, EmptyForm
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
    else:
        form = EmptyForm()
    return render_template('user.html', user=user, posts=posts, form=form)


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


@app.route('/delete_post', methods=['POST'])
@login_required
def delete_post():
    form = EmptyForm()
    pass


@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(u'User does not exist', 'danger')
            return redirect(url_for('user', username=username))
        if user == current_user:
            flash(u'You cannot follow yourself', 'danger')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(u'You are following {}'.format(user.username), 'success')
        return redirect(url_for('user', username=username))
    return redirect(url_for('index'))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(u'User does not exist', 'danger')
            return redirect(url_for('user', username=username))
        if user == current_user:
            flash(u'You cannot unfollow yourself', 'danger')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(u'You are not following {}'.format(user.username), 'success')
        return redirect(url_for('user', username=username))
    return redirect(url_for('index'))