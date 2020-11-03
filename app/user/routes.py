from flask import render_template, flash, request, redirect, url_for
from flask_login import current_user, login_required
from app import db
from app.models import User, Post
from app.forms import EmptyForm
from app.uploads.forms import UploadFileForm
from app.user import bp
from app.user.forms import AboutMeForm


@bp.route('/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.created_at.desc())
    if user == current_user:
        form = UploadFileForm()
    else:
        form = EmptyForm()
    return render_template('user/user.html', user=user, posts=posts, form=form)


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