from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, HiddenField
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


class EventImageForm(FlaskForm):
    image = FileField(lazy_gettext('Upload image'), validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], lazy_gettext('Images only'))
    ])
    submit = SubmitField(lazy_gettext('Update image'))


class EventUpdateForm(FlaskForm):
    title = StringField(lazy_gettext('Title'), validators=[
        DataRequired(gettext(u'This field is required.')),
        Length(min=3, max=254, message=gettext(u'Name must be between 3 and 254 characters.'))
    ])
    description = TextAreaField(lazy_gettext('Description'), validators=[])
    starts_at = DateTimeLocalField(lazy_gettext('Starts at'), validators=[
        DataRequired(gettext(u'This field is required.')),
    ])
    submit = SubmitField(lazy_gettext('Update event'))


class EventImageDeleteForm(FlaskForm):
    submit = SubmitField(lazy_gettext('Delete'))
