from datetime import datetime

from sqlalchemy.orm import relationship, backref

from app.extensions import db
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String


class Seat(db.Model):
    __tablename__ = 'seat'
    id = Column(Integer(), primary_key=True)
    x_axis = Column(String(255), nullable=False)
    y_axis = Column(String(255), nullable=False)
    status = Column(String(255), nullable=False, default='available')
    event_id = Column(Integer(), ForeignKey('event.id'), nullable=False)
    created_at = Column(DateTime(), default=datetime.utcnow)
    updated_at = Column(DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    event = relationship('Event', backref=backref('seats', lazy='joined'))
