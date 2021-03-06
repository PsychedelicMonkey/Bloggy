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
        share_form = EmptyForm()
        return render_template('index.html', title="Home", form=form, posts=posts.items, like_form=like_form, share_form=share_form, next_url=next_url, prev_url=prev_url)
    return render_template('index.html', title="Home", posts=posts.items, next_url=next_url, prev_url=prev_url)


@app.route('/latest')
def latest():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('latest', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('latest', page=posts.prev_num) if posts.has_prev else None
    if current_user.is_authenticated:
        form = PostForm()
        like_form = EmptyForm()
        share_form = EmptyForm()
        return render_template('index.html', title="Latest", form=form, posts=posts.items, like_form=like_form, share_form=share_form, next_url=next_url, prev_url=prev_url)
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


@app.route('/delete_post/<uuid>', methods=['GET', 'POST'])
@login_required
def delete_post(uuid):
    post = Post.query.filter_by(uuid=uuid).first()
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


#TODO: Toast
@app.route('/like/<uuid>', methods=['POST'])
@login_required
def like(uuid):
    post = Post.query.filter_by(uuid=uuid).first_or_404()
    form = EmptyForm()
    if form.validate_on_submit():
        if post.author == current_user:
            return jsonify({'message_category': 'danger', 'message': 'You cannot like your own posts'})
        if post.is_liked(current_user):
            return jsonify({'message_category': 'danger', 'message': 'You already like this post'})
        post.likes.append(current_user)
        db.session.commit()
        return jsonify({'likes': post.likes.count(), 'message_category': 'success', 'message': 'You liked {}\'s post'.format(post.author.first_name), 'action': url_for('unlike', uuid=uuid), 'btnLabel': '{} Likes'.format(post.likes.count()), 'btnClass': 'btn-danger'})


#TODO: Toast
@app.route('/unlike/<uuid>', methods=['POST'])
@login_required
def unlike(uuid):
    post = Post.query.filter_by(uuid=uuid).first_or_404()
    form = EmptyForm()
    if form.validate_on_submit():
        if post.author == current_user:
            return jsonify({'message_category': 'danger', 'message': 'You cannot unlike your own posts'})
        if not post.is_liked(current_user):
            return jsonify({'message_category': 'danger', 'message': 'You already unlike this post'})
        post.likes.remove(current_user)
        db.session.commit()
        return jsonify({'likes': post.likes.count(), 'message_category': 'success', 'message': 'You unliked {}\'s post'.format(post.author.first_name), 'action': url_for('like', uuid=uuid), 'btnLabel': '{} Likes'.format(post.likes.count()), 'btnClass': 'btn-success'})


#TODO: Toast and AJAX
@app.route('/share_post/<uuid>', methods=['POST'])
@login_required
def share_post(uuid):
    post = Post.query.filter_by(uuid=uuid).first_or_404()
    form = EmptyForm()
    if form.validate_on_submit():
        if post.author == current_user:
            flash(u'You cannot share your own posts', 'danger')
            return redirect(request.referrer)
        if current_user.is_sharing(post):
            flash(u'You are already sharing this post', 'danger')
            return redirect(request.referrer)
        post.shares.append(current_user)
        db.session.commit()
        flash(u'You are sharing {}\'s post'.format(post.author.first_name), 'success')
        return redirect(request.referrer)
    else:
        return redirect(url_for('index'))


#TODO: Toast and AJAX
@app.route('/unshare_post/<uuid>', methods=['POST'])
@login_required
def unshare_post(uuid):
    post = Post.query.filter_by(uuid=uuid).first_or_404()
    form = EmptyForm()
    if form.validate_on_submit():
        if post.author == current_user:
            flash(u'You cannot unshare your own posts', 'danger')
            return redirect(request.referrer)
        if not current_user.is_sharing(post):
            flash(u'You are already not sharing this post', 'danger')
            return redirect(request.referrer)
        post.shares.remove(current_user)
        db.session.commit()
        flash(u'You are no longer sharing {}\'s posts'.format(post.author.first_name), 'success')
        return redirect(request.referrer)
    else:
        return redirect(url_for('index'))


@app.route('/get_all_followers/<username>')
def get_all_followers(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    followers = user.followers.all()
    if user.followers.count() > 0:
        return render_template('modal/user/_followers.html', followers=followers, user=user, form=form, title='Followers')
    else:
        return 'No followers'


@app.route('/get_all_following/<username>')
def get_all_following(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    followers = user.followed.all()
    if user.followed.count() > 0:
        return render_template('modal/user/_followers.html', followers=followers, user=user, form=form, title='Follows')
    else:
        return 'No followers'


@app.route('/get_followers/<username>')
def get_followers(username):
    user = User.query.filter_by(username=username).first_or_404()
    followers = user.followers.limit(14)
    if followers.count() > 0:
        return render_template('user/_followers.html', followers=followers)
    else:
        return '<h5>{} has no followers</h5>'.format(user.first_name)


@app.route('/get_following/<username>')
def get_following(username):
    user = User.query.filter_by(username=username).first()
    followers = user.followed.limit(14)
    if followers.count() > 0:
        return render_template('user/_followers.html', followers=followers)
    else:
        return '<h5>{} is not following anyone</h5>'.format(user.first_name)


@app.route('/get_photos/<username>')
def get_photos(username):
    user = User.query.filter_by(username=username).first()
    photos = user.files.order_by(File.created_at.desc()).limit(6)
    file_path = app.config['UPLOAD_FOLDER']
    if photos:
        return render_template('user/gallery.html', user=user, photos=photos, folder=file_path)
    else:
        return '<h5>{} has no photos</h5>'.format(user.first_name)


@app.route('/new_post_modal')
def new_post_modal():
    return 'test'