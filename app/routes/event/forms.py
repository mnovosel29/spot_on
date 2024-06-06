from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.fields.datetime import DateTimeLocalField
from wtforms.validators import DataRequired, Length
from flask_babel import lazy_gettext, gettext


class EventCreateForm(FlaskForm):
    title = StringField(lazy_gettext('Title'), validators=[
        DataRequired(gettext(u'This field is required.')),
        Length(min=3, max=254, message=gettext(u'Name must be between 3 and 254 characters.'))
    ])
    description = TextAreaField(lazy_gettext('Description'), validators=[])
    starts_at = DateTimeLocalField(lazy_gettext('Starts at'), validators=[
        DataRequired(gettext(u'This field is required.')),
    ])
    submit = SubmitField(lazy_gettext('Add event'))
