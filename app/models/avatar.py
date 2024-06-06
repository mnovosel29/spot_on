from datetime import datetime

from sqlalchemy.orm import relationship, backref

from app.extensions import db
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text


class Avatar(db.Model):
    __tablename__ = 'avatar'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('user.id'), unique=True)
    image = Column(Text())
    created_at = Column(DateTime(), default=datetime.utcnow)
    updated_at = Column(DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    user = relationship('User', backref=backref('avatar', uselist=False), lazy='joined')
