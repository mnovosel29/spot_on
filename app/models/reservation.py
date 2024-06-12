from datetime import datetime

from sqlalchemy.orm import relationship, backref

from app.extensions import db
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String


class Reservation(db.Model):
    __tablename__ = 'reservation'
    id = Column(Integer(), primary_key=True)
    seat_id = Column(Integer(), ForeignKey('seat.id'), nullable=False)
    user_id = Column(Integer(), ForeignKey('user.id'), nullable=False)
    created_at = Column(DateTime(), default=datetime.utcnow)
    updated_at = Column(DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    seat = relationship('Seat', backref=backref('reserved_by', lazy='joined'))
    user = relationship('User', backref=backref('reservations', lazy='joined'))
