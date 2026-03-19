from .base_model import BaseModel
from app import db

place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey(
        'places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey(
        'amenities.id'), primary_key=True)
)


class Place(BaseModel):

    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    owner_id = db.Column(db.String(36), db.ForeignKey(
        'users.id'), nullable=False)

    reviews = db.relationship('Review', backref='place', lazy=True)
    amenities = db.relationship('Amenity', secondary=place_amenity, lazy='subquery',
                                backref=db.backref('places', lazy=True))
