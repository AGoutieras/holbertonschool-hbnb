#!/usr/bin/python3

from .base_model import BaseModel
from app import db

class Review(BaseModel):

    __tablename__ = 'reviews'

    text     = db.Column(db.Text, nullable=False)
    rating   = db.Column(db.Integer, nullable=False)
    user_id  = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'place_id', name='unique_user_place_review'),
    )