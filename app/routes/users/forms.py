from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_babel import lazy_gettext, gettext
from app.validators import Unique
from app.models.auth import User, Role


class UserCreateForm(FlaskForm):
    first_name = StringField(lazy_gettext('First name'), validators=[
        DataRequired(gettext(u'This field is required.')),
        Length(min=2, max=100, message=gettext(u'Name must be between 2 and 100 characters.'))
    ])
    last_name = StringField(lazy_gettext('Last name'), validators=[
        DataRequired(gettext(u'This field is required.')),
        Length(min=2, max=100, message=gettext(u'Name must be between 2 and 100 characters.'))
    ])
    email = StringField(lazy_gettext('Email'), validators=[
        DataRequired(gettext(u'This field is required.')),
        Email(gettext(u'Please enter a valid email address.')),
        Unique(model=User, field=User.email, message=gettext(u'This email is already in use.'))
    ])
    password = PasswordField(lazy_gettext('Password'), validators=[
        DataRequired(gettext(u'This field is required.')),
    ])
    confirm_password = PasswordField(lazy_gettext('Confirm Password'), validators=[
        DataRequired(gettext(u'This field is required.')),
        EqualTo('password', message=gettext(u'Passwords must match.'))
    ])
    submit = SubmitField(lazy_gettext('Add User'))


class UserInfoForm(FlaskForm):
    first_name = StringField(lazy_gettext('First name'), validators=[
        DataRequired(gettext(u'This field is required.')),
        Length(min=2, max=100, message=gettext(u'Name must be between 2 and 100 characters.'))
    ])
    last_name = StringField(lazy_gettext('Last name'), validators=[
        DataRequired(gettext(u'This field is required.')),
        Length(min=2, max=100, message=gettext(u'Name must be between 2 and 100 characters.'))
    ])
    submit = SubmitField(lazy_gettext('Update user'))


class UserEmailForm(FlaskForm):
    email = StringField(lazy_gettext('Email'), validators=[
        DataRequired(gettext(u'This field is required.')),
        Email(gettext(u'Please enter a valid email address.'))
    ])
    submit = SubmitField(lazy_gettext('Update email'))


class UserPasswordForm(FlaskForm):
    password = PasswordField(lazy_gettext('Password'), validators=[
        DataRequired(gettext(u'This field is required.')),
        Length(min=8, message=gettext(u'Password must be have at least 8 characters.'))
    ])
    confirm_password = PasswordField(lazy_gettext('Confirm Password'), validators=[
        DataRequired(gettext(u'This field is required.')),
        EqualTo('password', message=gettext(u'Passwords must match.'))
    ])
    submit = SubmitField(lazy_gettext('Update password'))


class UserAvatarForm(FlaskForm):
    avatar = FileField(lazy_gettext('Avatar'), validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], lazy_gettext('Images only'))
    ])
    submit = SubmitField(lazy_gettext('Update avatar'))


class UserAvatarDeleteForm(FlaskForm):
    submit = SubmitField(lazy_gettext('Delete avatar'))


class UserRolesForm(FlaskForm):
    roles = SelectMultipleField(lazy_gettext('Roles'), coerce=int)
    submit = SubmitField(lazy_gettext('Update roles'))


class UserActivateForm(FlaskForm):
    submit = SubmitField(lazy_gettext('Activate user'))


class UserDeactivateForm(FlaskForm):
    submit = SubmitField(lazy_gettext('Deactivate user'))


class UserConfirmForm(FlaskForm):
    submit = SubmitField(lazy_gettext('Confirm user'))


class UserDeleteForm(FlaskForm):
    submit = SubmitField(lazy_gettext('Delete user'))
