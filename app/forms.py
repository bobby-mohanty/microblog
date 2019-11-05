"""Forms for the app.

[description]
"""
from app.models import User

from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, TextAreaField, BooleanField,
                     SubmitField)
from wtforms.validators import (ValidationError, DataRequired, Email,
                                EqualTo, Length)


class LoginForm(FlaskForm):
    """Login form for user login.

    [description]
    """

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    """User registration form.

    [description]

    Extends:
        FlaskForm

    Variables:
        username {[type]} -- [description]
        email {[type]} -- [description]
        password {[type]} -- [description]
        password2 {[type]} -- [description]
        submit {[type]} -- [description]
    """

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        """User validation.

        [description]

        Arguments:
            username {[type]} -- [description]

        Raises:
            ValidationError -- [description]
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        """User email validation.

        [description]

        Arguments:
            email {[type]} -- [description]

        Raises:
            ValidationError -- [description]
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
    """Form to edit profile data.

    [description]

    Extends:
        FlaskForm

    Variables:
        username {[type]} -- [description]
        about_me {[type]} -- [description]
        submit {[type]} -- [description]
    """

    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        """Init edit profile form.

        [description]

        Arguments:
            original_username {[type]} -- [description]
            *args {[type]} -- [description]
            **kwargs {[type]} -- [description]
        """
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        """Validation for duplicate username.

        [description]

        Arguments:
            username {[type]} -- [description]

        Raises:
            ValidationError -- [description]
        """
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')
