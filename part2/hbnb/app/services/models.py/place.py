#!/usr/bin/python3

from .user import User
from .base_model import BaseModel



class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()

        if not isinstance(owner, User):
            raise ValueError("owner is not in User")

        if not isinstance(title, str) or not title.strip():
            raise ValueError("title must be a non-empty string")
        if len(title) > 100:
            raise ValueError("title must be at most 100 characters")
        self.title = title.strip()

        if not isinstance(price, (float, int)):
            raise ValueError("price must be a float or integer")

        if price <= 0:
            raise ValueError("price must be a positive value.")

        if not isinstance(latitude, (float, int)):
            raise ValueError("latitude must be float or integer")
        if not -90 <= latitude <= 90:
            raise ValueError("latitude -90 to 90")

        if not isinstance(longitude, (float, int)):
            raise ValueError("longitude must be float or integer")
        if not -180 <= longitude <= 180:
            raise ValueError("longitude -180 to 180")

        if description is None:
            self.description = None
        else:
            if not isinstance(description, str):
                raise ValueError("description must be a non-empty string")
            self.description = description.strip()


        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    def add_review(self, review):

        from .review import Review

        if not isinstance(review, Review):
            raise ValueError("review must be Review instance")
        if review.place is not self:
            raise ValueError("review.place must match this Place")

        if review not in self.reviews:
            self.reviews.append(review)
        self.save()


    def add_amenity(self, amenity):
        
        from .amenity import Amenity

        if not isinstance(amenity, Amenity):
            raise ValueError("amenity must be an Amenity instance")

        if amenity not in self.amenities:
            self.amenities.append(amenity)
        self.save()
