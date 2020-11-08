from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.auth import auth
from app.auth.forms import LoginForm, RegisterForm
from app.models import User

from app.unsplash.routes import get_random

from werkzeug.urls import url_parse

#TODO: Fix unsplash random image on login form
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(u'Username or password is incorrect.', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('auth/login.html', title='Login', form=form)
    #photo = get_random()
    #if photo:
    #    url = photo['urls']['regular']
    #    author = photo['user']['username']
    #    auth_link = photo['user']['links']['html']
    #    return render_template('auth/login.html', title="Login", form=form, url=url, author=author, auth_link=auth_link)
    #else:
    #    return render_template('auth/login.html', title="Login", form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'You are logged out', 'success')
    return redirect(url_for('index'))


#TODO: Fix unsplash random image on register form
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username = form.username.data.lower(),
            display_name = form.username.data,
            first_name = form.first_name.data.capitalize(),
            middle_name = form.middle_name.data.capitalize(),
            last_name = form.last_name.data.capitalize(),
            email = form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(u'You have registered!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)
    #photo = get_random()
    #if photo:
    #    url = photo['urls']['regular']
    #    author = photo['user']['username']
    #    auth_link = photo['user']['links']['html']
    #    return render_template('auth/register.html', title="Register", form=form, url=url, author=author, auth_link=auth_link)
    #else:
    #    return render_template('auth/register.html', title="Register", form=form)