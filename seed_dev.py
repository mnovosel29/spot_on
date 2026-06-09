import os
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

from app import create_app
from app.extensions import db
from app.models.auth import User, Role
from app.models.event import Event
from app.models.seat import Seat
from app.models.reservation import Reservation
from flask_security import SQLAlchemySessionUserDatastore
from flask_security.utils import hash_password
import uuid

app = create_app()

COLUMNS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S']
ROWS = [str(i) for i in range(1, 30)]  # 29 rows
DISABLED_COLUMNS = COLUMNS[-3:]        # Q, R, S

NORMAL_USERS = [
    {"email": "ana.horvat@example.com",  "first_name": "Ana",   "last_name": "Horvat", "password": "Password1!"},
    {"email": "ivan.kovac@example.com",  "first_name": "Ivan",  "last_name": "Kovač",  "password": "Password1!"},
    {"email": "maja.babic@example.com",  "first_name": "Maja",  "last_name": "Babić",  "password": "Password1!"},
    {"email": "luka.novak@example.com",  "first_name": "Luka",  "last_name": "Novak",  "password": "Password1!"},
    {"email": "petra.basic@example.com", "first_name": "Petra", "last_name": "Bašić",  "password": "Password1!"},
]

RESERVATION_PARTNERS = [
    ("Tomislav Horvat", "Ivana Horvat"),
    ("Marko Kovač",     "Sara Kovač"),
    ("Nikola Babić",    "Lucija Babić"),
    ("Filip Novak",     "Ema Novak"),
    ("Ante Bašić",      "Mia Bašić"),
]

with app.app_context():
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)

    # --- Admin role & user (required as event creator) ---
    admin_role = user_datastore.find_or_create_role(name="Admin", description="Administrator")

    email = os.environ.get("ADMIN_EMAIL")
    password = os.environ.get("ADMIN_PASSWORD")
    first_name = os.environ.get("ADMIN_FIRST_NAME", "Admin")
    last_name = os.environ.get("ADMIN_LAST_NAME", "Admin")

    if not email or not password:
        print("Error: ADMIN_EMAIL and ADMIN_PASSWORD must be set in .env")
        exit(1)

    existing_admin = user_datastore.find_user(email=email)
    if not existing_admin:
        admin_user = user_datastore.create_user(
            email=email,
            password=hash_password(password),
            first_name=first_name,
            last_name=last_name,
            active=True,
            confirmed_at=datetime.now(timezone.utc),
            fs_uniquifier=str(uuid.uuid4()),
            roles=[admin_role],
        )
        db.session.commit()
        print(f"Admin user created: {email}")
    else:
        admin_user = existing_admin
        admin_user.password = hash_password(password)
        admin_user.active = True
        admin_user.confirmed_at = admin_user.confirmed_at or datetime.now(timezone.utc)
        if admin_role not in admin_user.roles:
            admin_user.roles.append(admin_role)
        db.session.commit()
        print(f"Admin user updated: {email}")

    # --- Normal users ---
    normal_user_objects = []
    for u in NORMAL_USERS:
        existing = user_datastore.find_user(email=u["email"])
        if not existing:
            user = user_datastore.create_user(
                email=u["email"],
                password=hash_password(u["password"]),
                first_name=u["first_name"],
                last_name=u["last_name"],
                active=True,
                confirmed_at=datetime.now(timezone.utc),
                fs_uniquifier=str(uuid.uuid4()),
            )
            db.session.commit()
            print(f"User created: {u['email']}")
        else:
            user = existing
            print(f"User already exists: {u['email']}")
        normal_user_objects.append(user)

    # --- Event (app is hardcoded to event_id=1) ---
    event = Event.query.get(1)
    if not event:
        event = Event()
        event.title = "Rođendanski bal"
        event.description = "447. rođendan grada Karlovca"
        event.starts_at = datetime(2025, 6, 21, 20, 0, 0)
        event.creator_id = admin_user.id
        db.session.add(event)
        db.session.commit()
        print(f"Event created: {event.title} (id={event.id})")
    else:
        print(f"Event already exists: {event.title} (id={event.id})")

    # --- Seats (29 rows x 19 cols, last 3 cols disabled) ---
    existing_seats = Seat.query.filter_by(event_id=event.id).count()
    if existing_seats == 0:
        for y in ROWS:
            for x in COLUMNS:
                seat = Seat()
                seat.x_axis = x
                seat.y_axis = y
                seat.event_id = event.id
                seat.status = 'not_available' if x in DISABLED_COLUMNS else 'available'
                db.session.add(seat)
        db.session.commit()
        total = len(ROWS) * len(COLUMNS)
        disabled = len(ROWS) * len(DISABLED_COLUMNS)
        print(f"Seats created: {total} total, {disabled} disabled (columns {', '.join(DISABLED_COLUMNS)})")
    else:
        print(f"Seats already exist for event {event.id} ({existing_seats} seats), skipping")

    # --- Reservations (one per normal user on the first available seat) ---
    available_seats = Seat.query.filter_by(event_id=event.id, status='available').order_by(Seat.id).all()
    available_iter = iter(available_seats)

    for user, (partner_1, partner_2) in zip(normal_user_objects, RESERVATION_PARTNERS):
        existing_res = Reservation.query.filter_by(user_id=user.id).first()
        if existing_res:
            print(f"Reservation already exists for {user.email}, skipping")
            continue

        seat = next(available_iter, None)
        if seat is None:
            print(f"No available seats left for {user.email}")
            continue

        reservation = Reservation()
        reservation.seat_id = seat.id
        reservation.user_id = user.id
        reservation.partner_1 = partner_1
        reservation.partner_2 = partner_2
        db.session.add(reservation)

        seat.status = 'occupied'
        db.session.add(seat)
        db.session.commit()

        print(f"Reservation created: {user.email} → seat {seat.x_axis}{seat.y_axis} ({partner_1} & {partner_2})")

    print("Dev seed complete.")
