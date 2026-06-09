from app.extensions import db
from app.routes.seat import bp
from flask import redirect, url_for, flash
from flask_security import roles_required
from flask_babel import gettext

from app.models.seat import Seat
from app.models.reservation import Reservation


@bp.route('/<int:seat_id>/change_status', methods=['POST'])
@roles_required('Admin')
def change_status(seat_id):
    seat = Seat.query.get(seat_id)
    if seat.status == 'not_available':
        seat.status = 'available'
    elif seat.status == 'available':
        seat.status = 'not_available'
    else:
        flash(gettext('Seat status is invalid'), 'error')
        return redirect(url_for('event.seats', event_id=seat.event_id))

    db.session.commit()
    flash(gettext('Seat status updated'), 'success')

    return redirect(url_for('event.seats', event_id=seat.event_id))


@bp.route('/<int:seat_id>/admin_remove_reservation', methods=['POST'])
@roles_required('Admin')
def admin_remove_reservation(seat_id):
    seat = Seat.query.get(seat_id)
    reservation = Reservation.query.filter_by(seat_id=seat_id).first()
    if not reservation:
        flash(gettext('Reservation not found'), 'error')
        return redirect(url_for('event.seats', event_id=seat.event_id))

    db.session.delete(reservation)
    seat.status = 'available'
    db.session.commit()
    flash(gettext('Reservation removed'), 'success')

    return redirect(url_for('event.seats', event_id=seat.event_id))
