from flask import render_template, flash, request, redirect, url_for
from flask_login import current_user, login_required
from app import app, db
from app.models import User, Post
from app.forms import EmptyForm
from app.uploads.forms import UploadFileForm
from app.user import bp
from app.user.forms import AboutMeForm
from app.uploads.routes import allowed_file

import os
from glob import glob
from werkzeug.utils import secure_filename

@bp.route('/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.created_at.desc())
    photos = glob('{}/{}*'.format(app.config['UPLOAD_FOLDER'], user.username))
    like_form = EmptyForm()
    if user == current_user:
        form = UploadFileForm()
    else:
        form = EmptyForm()
    return render_template('user/user.html', user=user, posts=posts, photos=photos, form=form, like_form=like_form)


@bp.route('/<username>/photos')
def photos(username):
    user = User.query.filter_by(username=username).first_or_404()
    photos = glob('{}/{}*'.format(app.config['UPLOAD_FOLDER'], username))
    form = UploadFileForm()
    change_photo_form = EmptyForm()
    return render_template('user/photos.html', user=user, form=form, photos=photos, change_photo_form=change_photo_form)


@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(u'User does not exist', 'danger')
            return redirect(url_for('user.user', username=username))
        if user == current_user:
            flash(u'You cannot follow yourself', 'danger')
            return redirect(url_for('user.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(u'You are following {}'.format(user.username), 'success')
        return redirect(url_for('user.user', username=username))
    return redirect(url_for('index'))


@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(u'User does not exist', 'danger')
            return redirect(url_for('user.user', username=username))
        if user == current_user:
            flash(u'You cannot unfollow yourself', 'danger')
            return redirect(url_for('user.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(u'You are not following {}'.format(user.username), 'success')
        return redirect(url_for('user.user', username=username))
    return redirect(url_for('index'))


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = User.query.filter_by(username=current_user.username).first()
    form = AboutMeForm()
    if form.validate_on_submit():
        user.about_me = form.text.data
        db.session.commit()
        flash(u'Your \'About Me\' section is updated', 'success')
        return redirect(url_for('user.user', username=user.username))
    elif request.method == 'GET':
        form.text.data = user.about_me
    return render_template('user/forms/edit_profile.html', user=user, form=form)


#TODO: Change this function to just change the profile image
@bp.route('/change_profile_image', methods=['POST'])
@login_required
def change_profile_image():
    form = UploadFileForm()
    if form.validate_on_submit():
        if 'file' not in request.files:
            flash(u'No file was found!', 'danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash(u'No selected file', 'danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename('{}-{}'.format(current_user.username, file.filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            current_user.avatar = filename
            db.session.commit()
            return redirect(request.referrer)
    else:
        flash(u'Error', 'danger')
        return redirect(request.referrer)


#TODO: Change this function to just change the background image
@bp.route('/change_profile_background', methods=['POST'])
@login_required
def change_profile_background():
    form = UploadFileForm()
    if form.validate_on_submit():
        if 'file' not in request.files:
            flash(u'No file was found!', 'danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash(u'No selected file', 'danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename('{}-{}'.format(current_user.username, file.filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            current_user.background_image = filename
            db.session.commit()
            return redirect(request.referrer)
    else:
        flash(u'Error', 'danger')
        return redirect(request.referrer)