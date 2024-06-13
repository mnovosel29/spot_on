from flask import render_template, redirect, url_for, send_file, Response, current_app as app
from flask_babel import gettext
from flask_login import login_required, current_user
from app.extensions import db, mail
from app.models.seat import Seat
from app.models.reservation import Reservation
from flask_security import roles_required
from app.routes.home.forms import ReserveSeatForm, RemoveReservationForm
from app.services import ConfirmationService
from flask_mail import Mail, Message
import os

from app.routes.home import bp


@bp.route('/')
def index():
    seats = Seat.query.filter_by(event_id=1).order_by(Seat.id).all()
    total_seats = len([seat for seat in seats if seat.status != 'not_available'])
    reserved_seats = len([seat for seat in seats if seat.status == 'occupied'])
    reserve_seat_form = ReserveSeatForm()
    remove_reservation_form = RemoveReservationForm()
    if current_user.is_authenticated:
        my_reservations = Reservation.query.filter_by(user_id=current_user.id).all()
        my_reservations_ids = [reservation.seat_id for reservation in my_reservations]
        for seat in seats:
            if seat.id in my_reservations_ids:
                seat.status = 'my_position'
    return render_template('home/index.html',
                           seats=seats,
                           total_seats=total_seats,
                           reserved_seats=reserved_seats,
                           reserve_seat_form=reserve_seat_form,
                           remove_reservation_form=remove_reservation_form
                           )


@bp.route('/reserve/<int:seat_id>', methods=['POST'])
@login_required
def reserve(seat_id):
    seat = Seat.query.get(seat_id)
    reserve_seat_form = ReserveSeatForm()
    if reserve_seat_form.validate_on_submit():
        if seat.status == 'available':
            reservation = Reservation()
            reservation.seat_id = seat_id
            reservation.user_id = current_user.id
            reservation.partner_1 = reserve_seat_form.partner_1.data
            reservation.partner_2 = reserve_seat_form.partner_2.data
            db.session.add(reservation)
            db.session.commit()

            seat.status = 'occupied'
            db.session.add(seat)
            db.session.commit()

            output_dir = os.path.join(app.root_path, 'static', 'pdfs')
            filename = gettext("potvrda_rezervacije_") + seat.x_axis + seat.y_axis + ".pdf"
            confirmation_service = ConfirmationService(seat, reservation, output_dir, filename)
            confirmation_service.create_confirmation()

            msg = Message(gettext("Reservation Confirmation"),
                          recipients=[current_user.email])

            with app.open_resource(os.path.join(output_dir, filename)) as fp:
                msg.attach(filename, "application/pdf", fp.read())

            mail.send(msg)

    return redirect(url_for('home.index'))


@bp.route('/remove_reservation/<int:seat_id>', methods=['POST'])
@login_required
def remove_reservation(seat_id):
    seat = Seat.query.get(seat_id)
    reservation = Reservation.query.filter_by(seat_id=seat_id).first()
    if reservation.user_id != current_user.id:
        return redirect(url_for('home.index'))

    db.session.delete(reservation)
    db.session.commit()

    seat.status = 'available'
    db.session.add(seat)
    db.session.commit()

    return redirect(url_for('home.index'))


@bp.route('/confirmation/<int:seat_id>')
@login_required
def confirmation(seat_id):
    seat = Seat.query.get(seat_id)
    reservation = Reservation.query.filter_by(seat_id=seat_id).first()
    output_dir = os.path.join(app.root_path, 'static', 'pdfs')
    filename = gettext("potvrda_rezervacije_") + seat.x_axis + seat.y_axis + ".pdf"
    confirmation_service = ConfirmationService(seat, reservation, output_dir, filename)
    confirmation_service.create_confirmation()

    # Return the PDF as a response
    response = send_file(os.path.join(output_dir, filename), as_attachment=True)
    response.headers["Content-Disposition"] = "attachment; filename=" + filename
    return response


@bp.route('/check_reservation/<string:reservation_code>')
@roles_required('Admin')
def check_reservation(reservation_code):
    reservation = Reservation.query.filter_by(reservation_code=reservation_code).first()
    if reservation:
        return f"Reservation for seat {reservation.seat_id} is confirmed."
    return "Reservation not found."
