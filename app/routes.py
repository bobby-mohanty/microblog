"""Routes or endpoints for the app.

[description]
"""
from app import app

from flask import render_template, flash, redirect, url_for
from app.froms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    """Index page of the app.

    [description]

    Decorators:
        app.route
        app.route

    Returns:
        [type] -- [description]
    """
    user = {'username': 'Bobby'}
    posts = [
        {
            'author': {'username': 'Avengers'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page for the app.

    [description]

    Decorators:
        app.route

    Returns:
        [type] -- [description]
    """
    form = LoginForm()
    if form.validate_on_submit():
        flash('login requested for user {}, remember_me = {}'.format(
              form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
