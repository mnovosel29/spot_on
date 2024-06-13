from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, HiddenField, IntegerField
from wtforms.fields.datetime import DateTimeLocalField
from wtforms.validators import DataRequired, Length
from flask_babel import lazy_gettext, gettext


class ReserveSeatForm(FlaskForm):
    partner_1 = StringField(lazy_gettext('Partner 1'), validators=[DataRequired(), Length(min=2, max=255)])
    partner_2 = StringField(lazy_gettext('Partner 2'), validators=[DataRequired(), Length(min=2, max=255)])
    submit = SubmitField(lazy_gettext('Reserve'))


class RemoveReservationForm(FlaskForm):
    submit = SubmitField(lazy_gettext('Remove reservation'))
