import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        
        from app.services import facade
        facade.user_repo._storage.clear()
        facade.place_repo._storage.clear()
        facade.review_repo._storage.clear()
        facade.amenity_repo._storage.clear()

        # Create a user for all tests
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        self.user_id = response.get_json()['id']

        # Create a place for all tests
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })
        self.place_id = response.get_json()['id']

        # Create a review for all tests
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.review_id = response.get_json()['id']

        # Create an amenity for all tests
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Wi-Fi",
        })
        self.amenity_id = response.get_json()['id']

    # -------------------------------------------------------------
    # ------------------------ POST TESTS -------------------------
    # -------------------------------------------------------------

    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "doe.john@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Wi-Fi",
        })
        self.assertEqual(response.status_code, 201)

    def test_create_invalid_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "",
        })
        self.assertEqual(response.status_code, 400)

    def test_create_amenity_too_long(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "A" * 51,
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place(self):
        response_place = self.client.post('/api/v1/places/', json={
            "id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })
        self.assertEqual(response_place.status_code, 201)

    def test_create_place_invalid_price(self):
        response_place = self.client.post('/api/v1/places/', json={
            "id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": -100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })
        self.assertEqual(response_place.status_code, 400)

    def test_create_place_no_owner(self):
        response_place = self.client.post('/api/v1/places/', json={
            "id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": "non-existent-id"
        })
        self.assertEqual(response_place.status_code, 400)

    def test_create_review(self):
        response_review = self.client.post('/api/v1/reviews/', json={
            "id": "2fa85f64-5717-4562-b3fc-2c963f66afa6",
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response_review.status_code, 201)

    def test_create_review_invalid_rating(self):
        response_review = self.client.post('/api/v1/reviews/', json={
            "id": "2fa85f64-5717-4562-b3fc-2c963f66afa6",
            "text": "Great place to stay!",
            "rating": 0,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response_review.status_code, 400)

    # -------------------------------------------------------------
    # ------------------------- GET TESTS -------------------------
    # -------------------------------------------------------------

    def test_get_user(self):
        response_user = self.client.get(f'/api/v1/users/{self.user_id}')
        self.assertEqual(response_user.status_code, 200)

    def test_get_user_invalid(self):
        response_user = self.client.get('/api/v1/users/fake-user-id')
        self.assertEqual(response_user.status_code, 404)

    def test_get_all_users(self):
        response_user = self.client.get('/api/v1/users/')
        self.assertEqual(response_user.status_code, 200)

    def test_get_amenity(self):
        response_amenity = self.client.get(f'/api/v1/amenities/{self.amenity_id}')
        self.assertEqual(response_amenity.status_code, 200)
    
    def test_get_amenity_invalid(self):
        response_amenity = self.client.get('/api/v1/amenities/fake-amenity-id')
        self.assertEqual(response_amenity.status_code, 404)

    def test_get_all_amenities(self):
        response_user = self.client.get('/api/v1/amenities/')
        self.assertEqual(response_user.status_code, 200)

    def test_get_place(self):
        response_place = self.client.get(f'/api/v1/places/{self.place_id}')
        self.assertEqual(response_place.status_code, 200)

    def test_get_place_invalid(self):
        response_place = self.client.get('/api/v1/places/fake-place-id')
        self.assertEqual(response_place.status_code, 404)

    def test_get_all_places(self):
        response_user = self.client.get('/api/v1/places/')
        self.assertEqual(response_user.status_code, 200)

    def test_get_review(self):
        response_review = self.client.get(f'/api/v1/reviews/{self.review_id}')
        self.assertEqual(response_review.status_code, 200)

    def test_get_review_invalid(self):
        response_review = self.client.get('/api/v1/reviews/fake-review-id')
        self.assertEqual(response_review.status_code, 404)

    def test_get_all_reviews(self):
        response_user = self.client.get('/api/v1/reviews/')
        self.assertEqual(response_user.status_code, 200)

    # -------------------------------------------------------------
    # ------------------------- PUT TESTS -------------------------
    # -------------------------------------------------------------

    def test_put_amenity(self):
        response_amenity = self.client.put(f'/api/v1/amenities/{self.amenity_id}', json={
            "name": "Air Conditioning",
        })
        self.assertEqual(response_amenity.status_code, 200)

    def test_put_amenity_invalid(self):
        response_amenity = self.client.put('/api/v1/amenities/fake-amenity-id', json={
            "name": "Air Conditioning",
        })
        self.assertEqual(response_amenity.status_code, 404)

    def test_put_user(self):
        response_user = self.client.put(f'/api/v1/users/{self.user_id}', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response_user.status_code, 200)

    def test_put_user_invalid(self):
        response_user = self.client.put('/api/v1/users/fake-user-id', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response_user.status_code, 404)

    def test_put_place(self):
        response_place = self.client.put(f'/api/v1/places/{self.place_id}', json={
            "title": "Luxury Condo",
            "description": "An upscale place to stay",
            "price": 200.0
        })
        self.assertEqual(response_place.status_code, 200)

    def test_put_place_invalid(self):
        response_place = self.client.put('/api/v1/places/fake-place-id', json={
            "title": "Luxury Condo",
        })
        self.assertEqual(response_place.status_code, 404)

    def test_put_review(self):
        response_review = self.client.put(f'/api/v1/reviews/{self.review_id}', json={
            "text": "Amazing stay!",
            "rating": 4
        })
        self.assertEqual(response_review.status_code, 200)

    def test_put_review_invalid(self):
        response_review = self.client.put('/api/v1/reviews/fake-review-id', json={
            "text": "Amazing stay!",
            "rating": 4
        })
        self.assertEqual(response_review.status_code, 404)

    # -------------------------------------------------------------
    # ------------------------ DELETE TESTS -----------------------
    # -------------------------------------------------------------

    def test_delete_review(self):
        response_user = self.client.delete(f'/api/v1/reviews/{self.review_id}')
        self.assertEqual(response_user.status_code, 200)

    def test_delete_review_invalid(self):
        response_user = self.client.delete('/api/v1/reviews/fake-review-id')
        self.assertEqual(response_user.status_code, 404)
