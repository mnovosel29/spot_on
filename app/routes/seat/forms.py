from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, HiddenField, IntegerField
from wtforms.fields.datetime import DateTimeLocalField
from wtforms.validators import DataRequired, Length
from flask_babel import lazy_gettext, gettext


class SeatNotAvailableForm(FlaskForm):
    submit = SubmitField(lazy_gettext('Make not available'))


class SeatAvailableForm(FlaskForm):
    submit = SubmitField(lazy_gettext('Make available'))