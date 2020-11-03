from datetime import datetime
from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_required
from app import app, db
from app.forms import PostForm, EmptyForm
from app.models import Post

@app.before_request
def update_last_seen():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    if current_user.is_authenticated:
        form = PostForm()
        like_form = EmptyForm()
        return render_template('index.html', form=form, posts=posts, like_form=like_form)
    return render_template('index.html', posts=posts)


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


#TODO: Write the delete_post function
@app.route('/delete_post', methods=['POST'])
@login_required
def delete_post():
    form = EmptyForm()
    pass

@app.route('/like/<id>', methods=['POST'])
@login_required
def like(id):
    post = Post.query.filter_by(id=id).first_or_404()
    form = EmptyForm()
    if form.validate_on_submit():
        if post.author == current_user:
            flash(u'You cannot like your own posts', 'danger')
            return redirect(url_for('index'))
        if post.is_liked(current_user):
            flash(u'You already like this post', 'danger')
            return redirect(url_for('index'))
        post.likes.append(current_user)
        db.session.commit()
        flash(u'You liked {}\'s post'.format(post.author.display_name), 'success')
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@app.route('/unlike/<id>', methods=['POST'])
@login_required
def unlike(id):
    post = Post.query.filter_by(id=id).first_or_404()
    form = EmptyForm()
    if form.validate_on_submit():
        if post.author == current_user:
            flash(u'You cannot unlike your own posts', 'danger')
            return redirect(url_for('index'))
        if not post.is_liked(current_user):
            flash(u'You already unlike this post', 'danger')
            return redirect(url_for('index'))
        post.likes.remove(current_user)
        db.session.commit()
        flash(u'You unliked {}\'s post'.format(post.author.display_name), 'success')
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))