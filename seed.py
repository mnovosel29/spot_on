import os
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

from app import create_app
from app.extensions import db
from app.models.auth import User, Role
from flask_security import SQLAlchemySessionUserDatastore
from flask_security.utils import hash_password
import uuid

app = create_app()

with app.app_context():
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)

    admin_role = user_datastore.find_or_create_role(name="Admin", description="Administrator")

    email = os.environ.get("ADMIN_EMAIL")
    password = os.environ.get("ADMIN_PASSWORD")
    first_name = os.environ.get("ADMIN_FIRST_NAME", "Admin")
    last_name = os.environ.get("ADMIN_LAST_NAME", "Admin")

    if not email or not password:
        print("Error: ADMIN_EMAIL and ADMIN_PASSWORD must be set in .env")
        exit(1)

    existing = user_datastore.find_user(email=email)
    if not existing:
        user_datastore.create_user(
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
        existing.password = hash_password(password)
        existing.active = True
        existing.confirmed_at = existing.confirmed_at or datetime.now(timezone.utc)
        if admin_role not in existing.roles:
            existing.roles.append(admin_role)
        db.session.commit()
        print(f"Admin user updated: {email}")
