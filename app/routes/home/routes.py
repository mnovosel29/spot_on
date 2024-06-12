from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app.extensions import db
from app.models.seat import Seat
from app.models.reservation import Reservation
from flask_security import roles_required
from app.routes.home.forms import ReserveSeatForm

from app.routes.home import bp


@bp.route('/')
def index():
    seats = Seat.query.filter_by(event_id=1).order_by(Seat.id).all()
    reserve_seat_form = ReserveSeatForm()
    if current_user.is_authenticated:
        my_reservations = Reservation.query.filter_by(user_id=current_user.id).all()
        my_reservations_ids = [reservation.seat_id for reservation in my_reservations]
        for seat in seats:
            if seat.id in my_reservations_ids:
                seat.status = 'my_position'
    return render_template('home/index.html',
                           seats=seats,
                           reserve_seat_form=reserve_seat_form
                           )


@bp.route('/reserve/<int:seat_id>', methods=['POST'])
@login_required
def reserve(seat_id):
    seat = Seat.query.get(seat_id)
    if seat.status == 'available':
        reservation = Reservation()
        reservation.seat_id = seat_id
        reservation.user_id = current_user.id
        db.session.add(reservation)
        db.session.commit()

        seat.status = 'occupied'
        db.session.add(seat)
        db.session.commit()

    return redirect(url_for('home.index'))
