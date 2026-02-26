import re
from .base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()

        if not isinstance(first_name, str) or not first_name.strip():
            raise ValueError("first_name must be a non-empty string")
        if len(first_name) > 50:
            raise ValueError("first_name must be at most 50 characters")

        
        if not isinstance(last_name, str) or not last_name.strip():
            raise ValueError("Last_name must be a non-empty string")
        if len(last_name) > 50:
            raise ValueError("Last_name must be at most 50 characters")
        
        if not isinstance(email, str) or not email.strip():
            raise ValueError("email must be a non-empty string")
        email = email.strip()
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            raise ValueError("email must be a valid email address")

        if not isinstance(is_admin, bool):
            raise ValueError("is_admin must be a boolean")

        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.email = email.strip()
        self.is_admin = is_admin
