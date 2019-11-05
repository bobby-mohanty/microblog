"""Errors for the app."""

from flask import render_template
from app import app, db


@app.errorhandler(404)
def not_found_error(error):
    """Not found error.

    [description]

    Decorators:
        app.errorhandler

    Arguments:
        error {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Internal server error.

    [description]

    Decorators:
        app.errorhandler

    Arguments:
        error {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    db.session.rollback()
    return render_template('500.html'), 500
