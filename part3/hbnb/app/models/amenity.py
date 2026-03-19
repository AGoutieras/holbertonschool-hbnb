#!/usr/bin/python3

from .base_model import BaseModel
from app import db

class Amenity(BaseModel):

    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False, unique=True)