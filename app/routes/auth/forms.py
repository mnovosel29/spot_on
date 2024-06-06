from flask_security import RegisterForm
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_babel import lazy_gettext, gettext
from app.validators import Unique
from app.models.auth import User


class ExtendedRegisterForm(RegisterForm):
    first_name = StringField(lazy_gettext('First name'), validators=[
        DataRequired(gettext(u'This field is required.')),
        Length(min=2, max=100, message=gettext(u'First name must be between 2 and 100 characters.'))
    ])
    last_name = StringField(lazy_gettext('Last name'), validators=[
        DataRequired(gettext(u'This field is required.')),
        Length(min=2, max=100, message=gettext(u'Last name must be between 2 and 100 characters.'))
    ])
    email = StringField(lazy_gettext('Email'), validators=[
        DataRequired(gettext(u'This field is required.')),
        Email(gettext(u'Please enter a valid email address.')),
        Unique(model=User, field=User.email, message=gettext(u'This email is already in use.'))
    ])
    password = PasswordField(lazy_gettext('Password'), validators=[
        DataRequired(gettext(u'This field is required.')),
    ])
    password_confirm = PasswordField(lazy_gettext('Confirm Password'), validators=[
        DataRequired(gettext(u'This field is required.')),
        EqualTo('password', message=gettext(u'Passwords must match.'))
    ])
    submit = SubmitField(lazy_gettext('Sign Up'))


class LoginForm(FlaskForm):
    email = StringField(lazy_gettext('Email'), validators=[
        DataRequired(gettext(u'This field is required.')),
        Email(gettext(u'Please enter a valid email address.'))
    ])
    password = PasswordField(lazy_gettext('Password'), validators=[
        DataRequired(gettext(u'This field is required.'))
    ])
    submit = SubmitField(lazy_gettext('Login'))


class ProfileForm(FlaskForm):
    first_name = StringField(lazy_gettext('First name'), validators=[
        DataRequired(gettext(u'This field is required.')),
        Length(min=2, max=100, message=gettext(u'First name must be between 2 and 100 characters.'))
    ])
    last_name = StringField(lazy_gettext('Last name'), validators=[
        DataRequired(gettext(u'This field is required.')),
        Length(min=2, max=100, message=gettext(u'Last name must be between 2 and 100 characters.'))
    ])
    submit = SubmitField(lazy_gettext('Update'))


class EmailForm(FlaskForm):
    email = StringField(lazy_gettext('Email'), validators=[
        DataRequired(gettext(u'This field is required.')),
        Email(gettext(u'Please enter a valid email address.')),
        Unique(model=User, field=User.email, message=gettext(u'This email is already in use.'))
    ])
    submit = SubmitField(lazy_gettext('Update'))


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(lazy_gettext('Current Password'), validators=[
        DataRequired(gettext(u'This field is required.')),
    ])
    password = PasswordField(lazy_gettext('Password'), validators=[
        DataRequired(gettext(u'This field is required.')),
    ])
    confirm_password = PasswordField(lazy_gettext('Confirm Password'), validators=[
        DataRequired(gettext(u'This field is required.')),
        EqualTo('password', message=gettext(u'Passwords must match.'))
    ])
    submit = SubmitField(lazy_gettext('Update'))


class ForgotPasswordForm(FlaskForm):
    email = StringField(lazy_gettext('Email'), validators=[
        DataRequired(gettext(u'This field is required.')),
        Email(gettext(u'Please enter a valid email address.'))
    ])
    submit = SubmitField(lazy_gettext('Reset Password'))


class AvatarForm(FlaskForm):
    avatar = FileField(lazy_gettext('Avatar'), validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], lazy_gettext('Images only'))
    ])
    submit = SubmitField(lazy_gettext('Update avatar'))


class AvatarDeleteForm(FlaskForm):
    submit = SubmitField(lazy_gettext('Delete avatar'))
