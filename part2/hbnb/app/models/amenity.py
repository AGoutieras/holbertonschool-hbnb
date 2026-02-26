from .base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")
        if len(name) > 50:
            raise ValueError("name must be at most 50 characters")

        self.name = name.strip()
