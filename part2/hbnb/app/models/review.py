#!/usr/bin/python3

from .place import Place
from .user import User
from .base_model import BaseModel


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()

        if not isinstance(text, str) or not text.strip():
            raise ValueError("text must be a non-empty string")
        
        if not isinstance(rating, int):
            raise ValueError("rating must be a integer")
        if not 1 <= rating <= 5:
            raise ValueError("rating must be between 1 and 5.")
        
        if not isinstance(place, Place):
            raise ValueError("place must be a Place instance")
        
        if not isinstance(user, User):
            raise ValueError("user must be a User instance")

        self.text = text.strip()
        self.rating = rating
        self.place = place
        self.user = user
