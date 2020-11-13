from flask import render_template
from app.errors import error

@error.app_errorhandler(404)
def error_not_found(error):
    return render_template('errors/404.html', title='Page Not Found'), 404


@error.app_errorhandler(500)
def error_not_found(error):
    return render_template('errors/500.html', title='Server Error'), 500