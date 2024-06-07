from datetime import datetime

from sqlalchemy.orm import relationship, backref

from app.extensions import db
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text, Boolean


class EventImage(db.Model):
    __tablename__ = 'image'
    id = Column(Integer(), primary_key=True)
    event_id = Column(Integer(), ForeignKey('event.id'), nullable=False)
    is_title_image = Column(Boolean(), default=False, nullable=False)
    base_64 = Column(Text(), nullable=False)
    created_at = Column(DateTime(), default=datetime.utcnow)
    updated_at = Column(DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    event = relationship('Event', backref=backref('images'), lazy='joined')
