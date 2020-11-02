from flask import render_template, flash, redirect, url_for, request
from app.auth import auth
from app.auth.forms import LoginForm, RegisterForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(u'Login requested for user={}, remember_me={}'.format(form.username.data, form.remember_me.data), 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/login.html', title="Login", form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash(u'Registration requested for user={}, email={}'.format(form.username.data, form.email.data), 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title="Register", form=form)