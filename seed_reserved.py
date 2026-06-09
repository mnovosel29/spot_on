import os
from dotenv import load_dotenv

load_dotenv()

from app import create_app
from app.extensions import db
from app.models.seat import Seat
from app.models.reservation import Reservation
from flask_security import SQLAlchemySessionUserDatastore
from app.models.auth import User, Role

app = create_app()

# SQLite only supports one writer at a time.
# Stop the Flask dev server before running this script, then restart it.

RESERVED_ROWS = ['1', '2', '3', '4']
PARTNER_1 = 'Rezervirano'
PARTNER_2 = 'Grad Karlovac'

with app.app_context():
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)

    admin_email = os.environ.get("ADMIN_EMAIL")
    if not admin_email:
        print("Error: ADMIN_EMAIL must be set in .env")
        exit(1)

    admin_user = user_datastore.find_user(email=admin_email)
    if not admin_user:
        print(f"Error: Admin user '{admin_email}' not found. Run seed.py first.")
        exit(1)

    seats = (
        Seat.query
        .filter(Seat.event_id == 1, Seat.y_axis.in_(RESERVED_ROWS))
        .order_by(Seat.y_axis, Seat.x_axis)
        .all()
    )

    created = 0
    skipped = 0

    for seat in seats:
        if seat.status != 'available':
            skipped += 1
            continue

        existing = Reservation.query.filter_by(seat_id=seat.id).first()
        if existing:
            skipped += 1
            continue

        reservation = Reservation()
        reservation.seat_id = seat.id
        reservation.user_id = admin_user.id
        reservation.partner_1 = PARTNER_1
        reservation.partner_2 = PARTNER_2
        db.session.add(reservation)

        seat.status = 'occupied'
        db.session.add(seat)
        db.session.commit()

        print(f"Reserved seat {seat.x_axis}{seat.y_axis}")
        created += 1

    print(f"\nDone. Reserved: {created}, skipped: {skipped} (already occupied or unavailable).")
