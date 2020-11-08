from datetime import datetime
from flask import render_template, flash, redirect, request, url_for, jsonify
from flask_login import current_user, login_required
from app import app, db
from app.forms import PostForm, EmptyForm
from app.models import Post, User, File

import json

@app.before_request
def update_last_seen():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    if current_user.is_authenticated:
        posts = current_user.followed_posts().order_by(Post.created_at.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    else:
        posts = Post.query.order_by(Post.created_at.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
    if current_user.is_authenticated:
        form = PostForm()
        like_form = EmptyForm()
        return render_template('index.html', title="Home", form=form, posts=posts.items, like_form=like_form, next_url=next_url, prev_url=prev_url)
    return render_template('index.html', title="Home", posts=posts.items, next_url=next_url, prev_url=prev_url)


@app.route('/latest')
def latest():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
    if current_user.is_authenticated:
        form = PostForm()
        like_form = EmptyForm()
        return render_template('index.html', title="Latest", form=form, posts=posts.items, like_form=like_form, next_url=next_url, prev_url=prev_url)
    return render_template('index.html', title="Latest", posts=posts.items, next_url=next_url, prev_url=prev_url)


@app.route('/upload_post', methods=['POST'])
@login_required
def upload_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(u'Your post is live!', 'success')
        return redirect(request.referrer)
    else:
        return redirect(url_for('index'))


@app.route('/delete_post/<id>', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    form = EmptyForm()
    if form.validate_on_submit():
        db.session.delete(post)
        db.session.commit()
        flash(u'Your post was deleted', 'success')
        return redirect(request.referrer)
    elif request.method == 'GET':
        return render_template('modal/_delete_post.html', form=form, post=post)
    else:
        return redirect(url_for('index'))


#TODO: Change to include CRSF
@app.route('/like/<id>', methods=['POST'])
@login_required
def like(id):
    post = Post.query.filter_by(id=id).first_or_404()
    if post.author == current_user:
        return jsonify({'message_category': 'danger', 'message': 'You cannot like your own posts'})
    if post.is_liked(current_user):
        return jsonify({'message_category': 'danger', 'message': 'You already like this post'})
    post.likes.append(current_user)
    db.session.commit()
    return jsonify({'id': post.id, 'likes': post.likes.count(), 'message_category': 'success', 'message': 'You liked {}\'s post'.format(post.author.first_name)})
    #post = Post.query.filter_by(id=id).first_or_404()
    #form = EmptyForm()
    #if form.validate_on_submit():
    #    if post.author == current_user:
    #        flash(u'You cannot like your own posts', 'danger')
    #        return redirect(url_for('index'))
    #    if post.is_liked(current_user):
    #        flash(u'You already like this post', 'danger')
    #        return redirect(url_for('index'))
    #    post.likes.append(current_user)
    #    db.session.commit()
    #    flash(u'You liked {}\'s post'.format(post.author.display_name), 'success')
    #    return redirect(request.referrer)
    #else:
    #    return redirect(url_for('index'))


#TODO: Change to include CRSF
@app.route('/unlike/<id>', methods=['POST'])
@login_required
def unlike(id):
    post = Post.query.filter_by(id=id).first_or_404()
    if post.author == current_user:
        return jsonify({'message_category': 'danger', 'message': 'You cannot unlike your own posts'})
    if not post.is_liked(current_user):
        return jsonify({'message_category': 'danger', 'message': 'You already unlike this post'})
    post.likes.remove(current_user)
    db.session.commit()
    return jsonify({'id': post.id, 'likes': post.likes.count(), 'message_category': 'success', 'message': 'You unliked {}\'s post'.format(post.author.first_name)})
    #form = EmptyForm()
    #if form.validate_on_submit():
    #    if post.author == current_user:
    #        flash(u'You cannot unlike your own posts', 'danger')
    #        return redirect(url_for('index'))
    #    if not post.is_liked(current_user):
    #        flash(u'You already unlike this post', 'danger')
    #        return redirect(url_for('index'))
    #    post.likes.remove(current_user)
    #    db.session.commit()
    #    flash(u'You unliked {}\'s post'.format(post.author.display_name), 'success')
    #    return redirect(request.referrer)
    #else:
    #    return redirect(url_for('index'))


@app.route('/get_followers/<username>')
def get_followers(username):
    user = User.query.filter_by(username=username).first_or_404()
    followers = user.followers
    if followers.count() > 0:
        return render_template('user/_followers.html', followers=followers)
    else:
        return '<h5>{} has no followers</h5>'.format(user.first_name)


@app.route('/get_following/<username>')
def get_following(username):
    user = User.query.filter_by(username=username).first()
    followers = user.followed
    if followers.count() > 0:
        return render_template('user/_followers.html', followers=followers)
    else:
        return '<h5>{} is not following anyone</h5>'.format(user.first_name)


@app.route('/get_photos/<username>')
def get_photos(username):
    user = User.query.filter_by(username=username).first()
    photos = user.files.order_by(File.created_at.desc()).all()
    file_path = app.config['UPLOAD_FOLDER']
    if photos:
        return render_template('user/gallery.html', user=user, photos=photos, folder=file_path)
    else:
        return '<h5>{} has no photos</h5>'.format(user.first_name)


@app.route('/new_post_modal')
def new_post_modal():
    return 'test'