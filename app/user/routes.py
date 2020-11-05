from flask import render_template, flash, request, redirect, url_for
from flask_login import current_user, login_required
from app import app, db
from app.models import User, Post, File
from app.forms import EmptyForm
from app.uploads.forms import UploadFileForm
from app.user import bp
from app.user.forms import AboutMeForm
from app.uploads.routes import allowed_file

import os
from glob import glob
from werkzeug.utils import secure_filename

file_path = app.config['UPLOAD_FOLDER'].split('app')[1]

@bp.route('/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.created_at.desc())
    photos = current_user.files.order_by(File.created_at.desc()).all()
    #photos = glob('{}/{}*'.format(app.config['UPLOAD_FOLDER'], user.username))
    like_form = EmptyForm()
    about_me = AboutMeForm()
    form = EmptyForm()
    return render_template('user/user.html', user=user, posts=posts, photos=photos, folder=file_path, form=form, like_form=like_form, about_me=about_me)


@bp.route('/<username>/photos')
def photos(username):
    user = User.query.filter_by(username=username).first_or_404()
    photos = current_user.files.order_by(File.created_at.desc()).all()
    #photos = glob('{}/{}*'.format(app.config['UPLOAD_FOLDER'], username))
    form = UploadFileForm()
    return render_template('user/photos.html', user=user, form=form, photos=photos, folder=file_path)


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


@bp.route('/change_profile_image/<id>', methods=['GET', 'POST'])
@login_required
def change_profile_image(id):
    photo = File.query.filter_by(id=id).first()
    form = EmptyForm()
    if form.validate_on_submit():
        current_user.avatar = photo.name
        db.session.commit()
        flash(u'You changed your profile image', 'success')
        return redirect(request.referrer)
    elif request.method == 'GET':
        return render_template('modal/_change_profile_image.html', photo=photo, form=form, folder=file_path)
    else:
        return redirect(url_for('index'))


@bp.route('/change_profile_background/<id>', methods=['GET', 'POST'])
@login_required
def change_profile_background(id):
    photo = File.query.filter_by(id=id).first()
    form = EmptyForm()
    if form.validate_on_submit():
        current_user.background_image = photo.name
        db.session.commit()
        flash(u'You changed your background image', 'success')
        return redirect(request.referrer)
    elif request.method == 'GET':
        return render_template('modal/_change_profile_background.html', photo=photo, form=form, folder=file_path)
    else:
        return redirect(url_for('index'))


@bp.route('/delete_image/<id>', methods=['GET', 'POST'])
@login_required
def delete_image(id):
    form = EmptyForm()
    photo = File.query.filter_by(id=id).first()
    if form.validate_on_submit():
        if photo.name == current_user.avatar:
            current_user.avatar = ''
        elif photo.name == current_user.background_image:
            current_user.background_image = ''
        path = app.config['UPLOAD_FOLDER'] + '/' + photo.name
        if os.path.exists(path):
            os.remove(path)
            db.session.delete(photo)
            db.session.commit()
            flash(u'Your photo was deleted', 'success')
            return redirect(request.referrer)
        else:
            flash(u'Could not delete photo', 'danger')
            return redirect(request.referrer)
    elif request.method == 'GET':
        return render_template('modal/_delete_image.html', form=form, photo=photo, folder=file_path)
    else:
        return redirect(url_for('index'))


@bp.route('/edit_bio', methods=['GET', 'POST'])
@login_required
def edit_bio():
    user = User.query.filter_by(username=current_user.username).first()
    form = AboutMeForm()
    if form.validate_on_submit():
        user.about_me = form.text.data
        db.session.commit()
        flash(u'You \'About Me\' section is updated.', 'success')
        return redirect(url_for('user.user', username=user.username))
    elif request.method == 'GET':
        form.text.data = user.about_me
        return render_template('modal/_edit_bio.html', form=form)
    else:
        return redirect(url_for('index'))