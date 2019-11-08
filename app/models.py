"""Database structure for the app.

[description]
"""

from app import app, db, login

import jwt
from time import time
from hashlib import md5
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# The 'association table' foor the follower and followed relationship
followers = db.Table('followers',
                     db.Column('follower_id', db.Integer,
                               db.ForeignKey('user.id')),
                     db.Column('followed_id',
                               db.Integer, db.ForeignKey('user.id')))


class User(UserMixin, db.Model):
    """User table structure.

    [description]

    Extends:
        db.Model

    Variables:
        id {[type]} -- [description]
        username {[type]} -- [description]
        email {[type]} -- [description]
        password_hash {[type]} -- [description]
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        """Represtation of the User object.

        [description]
        """
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        """Set password.

        [description]

        Arguments:
            password {[type]} -- [description]
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify Password.

        [description]

        Arguments:
            password {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        """Get avatar for user.

        [description]

        Arguments:
            size {[type]} -- [description]
        """
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user):
        """Add user to following list.

        [description]

        Arguments:
            user {[type]} -- [description]
        """
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        """Remove user from following list.

        [description]

        Arguments:
            user {[type]} -- [description]
        """
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        """Check if a user is in following list or not.

        [description]

        Arguments:
            user {[type]} -- [description]
        """
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        """Get all the posts by the users being followed by the current user.

        [description]

        Returns:
            [type] -- [description]
        """
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        """Generate password reset jwt token."""
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        """Verify the jwt token for password reset."""
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Post(db.Model):
    """Posts table structure.

    [description]

    Extends:
        db.Model

    Variables:
        id {[type]} -- [description]
        body {[type]} -- [description]
        timestamp {[type]} -- [description]
        user_id {[type]} -- [description]
    """

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    language = db.Column(db.String(5))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        """Representation for Post object.

        [description]
        """
        return '<Post {}>'.format(self.body)


@login.user_loader
def load_user(id):
    """User loader function for app.

    The flask_login extension expects that the application will configure a
    user loader function, that can be called to load a user given the ID
    """
    return User.query.get(int(id))
