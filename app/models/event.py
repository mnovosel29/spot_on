from datetime import datetime

from sqlalchemy.orm import relationship, backref

from app.extensions import db
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text, String


def get_current_user():
    from flask_login import current_user
    return current_user.id


class Event(db.Model):
    __tablename__ = 'event'
    id = Column(Integer(), primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text(), nullable=True)
    image_id = Column(String(255), nullable=True)
    starts_at = Column(DateTime(), nullable=False)
    created_at = Column(DateTime(), default=datetime.utcnow)
    updated_at = Column(DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    creator_id = Column(Integer(), ForeignKey('user.id'), nullable=False, default=get_current_user)
    creator = relationship('User', backref=backref('events', lazy='joined'))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'starts_at': self.starts_at
        }
