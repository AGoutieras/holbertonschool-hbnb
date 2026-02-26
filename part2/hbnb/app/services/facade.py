from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ------------ USER METHODS ------------

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    # ------------ AMENITY METHODS ------------

    def create_amenity(self, amenity_data):
        name = amenity_data.get("name")
        if name is None:
            raise ValueError("name is required")
        new_amenity = Amenity(name)
        self.amenity_repo.add(new_amenity)
        return new_amenity

    def get_amenity(self, amenity_id):
        new_amenity_id = self.amenity_repo.get(amenity_id)
        return new_amenity_id

    def get_all_amenities(self):
        new_all_amenity = self.amenity_repo.get_all()
        return new_all_amenity

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError ("amenity not found")
        return self.amenity_repo.update(amenity_id, amenity_data)

    # ------------ PLACE METHODS ------------

    def create_place(self, place_data):
        owner = self.user_repo.get(place_data.get('owner_id'))
        if not owner:
            raise ValueError("Owner not found")

        amenities = []
        for a_id in place_data.get('amenities', []):
            amenity = self.amenity_repo.get(a_id)
            if not amenity:
                raise ValueError(f"Amenity {a_id} not found")
            amenities.append(amenity)

        place = Place(
            title=place_data['title'],
            description=place_data.get('description'),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner
        )

        for amenity in amenities:
            place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        return self.place_repo.update(place_id, place_data)

    # ------------ REVIEW METHODS ------------

    def create_review(self, review_data):
        user = self.user_repo.get(review_data.get('user_id'))
        place = self.place_repo.get(review_data.get('place_id'))

        if not user:
            raise ValueError("User not found")

        if not place:
            raise ValueError("Place not found")

        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place=place,
            user=user,
        )

        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        reviews = [review for review in self.review_repo.get_all() if review.place.id == place_id]
        return reviews

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        return self.review_repo.delete(review_id)
