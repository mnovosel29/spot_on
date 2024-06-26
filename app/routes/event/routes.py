from flask_babel import gettext

from app.extensions import db
from app.models.event_image import EventImage
from app.routes.event import bp
from app.routes.event.forms import (
    EventCreateForm,
    EventUpdateForm,
    EventImageForm,
    EventImageDeleteForm,
    EventDeleteForm,
    EventCreateSeatsForm
)

from app.services import ImageService
from flask import jsonify, request, render_template, flash, redirect, url_for
from flask_security import roles_required

from app.models.event import Event
from app.models.seat import Seat


@bp.route('/get_events', methods=['POST', 'GET'])
@roles_required('Admin')
def get_events():
    search = request.json.get('search', '')
    page = request.json.get('page', 1)
    per_page = request.json.get('per_page', 10)
    sort_by = request.json.get('sort_by', 'id')
    sort_direction = request.json.get('sort_direction', 'asc')
    order = getattr(Event, sort_by).desc() if sort_direction == 'desc' else getattr(Event, sort_by)

    events = Event.query.order_by(order).filter(Event.title.ilike(f'%{search}%')).paginate(page=int(page),
                                                                                           per_page=int(per_page))

    return jsonify({
        'items': [event.to_dict() for event in events.items],
        'total': events.total,
        'page': events.page,
        'per_page': events.per_page,
        'pages': events.pages,
    })


@bp.route('/')
@roles_required('Admin')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    events = Event.query.paginate(page=page, per_page=per_page)

    return render_template('admin/events/index.html', events=events)


@bp.route('/create', methods=['GET', 'POST'])
@roles_required('Admin')
def create():
    event_create_form = EventCreateForm()
    if event_create_form.validate_on_submit():
        new_event = Event()
        new_event.title = event_create_form.title.data
        new_event.description = event_create_form.description.data
        new_event.starts_at = event_create_form.starts_at.data
        db.session.add(new_event)
        db.session.commit()
        flash(gettext('Event created successfully.'), 'success')
        return redirect(url_for('event.index'))
    return render_template('admin/events/create.html', event_create_form=event_create_form)


@bp.route('/<int:event_id>')
@roles_required('Admin')
def detail(event_id):
    event = Event.query.get(event_id)
    event_update_form = EventUpdateForm(obj=event)
    event_image_form = EventImageForm()
    event_image_delete_form = EventImageDeleteForm()
    event_delete_form = EventDeleteForm()
    return render_template('admin/events/detail.html',
                           event_update_form=event_update_form,
                           event_image_form=event_image_form,
                           event_image_delete_form=event_image_delete_form,
                           event_delete_form=event_delete_form,
                           event=event)


@bp.route('/<int:event_id>/update', methods=['POST'])
@roles_required('Admin')
def update(event_id):
    event = Event.query.get(event_id)
    event_update_form = EventUpdateForm()
    if event_update_form.validate_on_submit():
        event.title = event_update_form.title.data
        event.description = event_update_form.description.data
        event.starts_at = event_update_form.starts_at.data
        db.session.commit()
        flash(gettext('Event updated successfully.'), 'success')
        return redirect(url_for('event.index'))
    return render_template('admin/events/detail.html',
                           event_update_form=event_update_form,
                           event=event
                           )


@bp.route('/<int:event_id>/add_image', methods=['POST'])
@roles_required('Admin')
def add_image(event_id):
    event_image_form = EventImageForm()
    if event_image_form.validate_on_submit():
        base64 = ImageService.get_base64(event_image_form.image.data)
        image = EventImage()
        image.base_64 = base64
        image.event_id = event_id
        db.session.add(image)
        db.session.commit()
        flash(gettext('Image added successfully.'), 'success')

    return redirect(url_for('event.detail', event_id=event_id))


@bp.route('/delete_image/<int:image_id>/', methods=['POST'])
@roles_required('Admin')
def delete_image(image_id):
    image = EventImage.query.get(image_id)
    event_id = image.event_id
    flash(image_id, 'success')
    db.session.delete(image)
    db.session.commit()
    flash(gettext('Image deleted successfully.'), 'success')
    return redirect(url_for('event.detail', event_id=event_id))


@bp.route('/<int:event_id>/delete', methods=['POST'])
@roles_required('Admin')
def delete(event_id):
    event = Event.query.get(event_id)
    db.session.delete(event)
    db.session.commit()
    flash(gettext('Event deleted successfully.'), 'success')
    return redirect(url_for('event.index'))


@bp.route('/<int:event_id>/seats', methods=['GET', 'POST'])
@roles_required('Admin')
def seats(event_id):
    event = Event.query.get(event_id)
    event_create_seats_form = EventCreateSeatsForm()
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
               'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    show_seats = False
    x_axis = []
    y_axis = []
    seats = Seat.query.filter_by(event_id=event_id).order_by(Seat.id).all()

    if seats:
        show_seats = True
        x_axis = sorted(list(set([seat.x_axis for seat in seats])))
        y_axis = sorted(list(set([seat.y_axis for seat in seats])))

    if event_create_seats_form.validate_on_submit():
        x_axis = letters[:event_create_seats_form.number_of_columns.data]
        y_axis = [str(i) for i in range(1, event_create_seats_form.number_of_rows.data + 1)]
        for y in y_axis:
            for x in x_axis:
                seat = Seat()
                seat.x_axis = x
                seat.y_axis = y
                seat.event_id = event_id
                db.session.add(seat)
                db.session.commit()
        flash(gettext('Seats created successfully.'), 'success')

    return render_template('admin/events/seats.html',
                           event=event,
                           event_create_seats_form=event_create_seats_form,
                           show_seats=show_seats,
                           x_axis=x_axis,
                           y_axis=y_axis,
                           seats=seats
                           )
