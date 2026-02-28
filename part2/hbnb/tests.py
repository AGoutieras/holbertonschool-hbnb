import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    # ------------ POSTS TESTS ------------

    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
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

    def test_invalid_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "",
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place(self):
        response_user = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response_user.status_code, 201)

        response_place = self.client.post('/api/v1/places/', json={
            "id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": response_user.get_json()['id'] 
        })
        self.assertEqual(response_place.status_code, 201)

    def test_create_review(self):
        response_user = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith@example.com"
        })
        self.assertEqual(response_user.status_code, 201)

        response_place = self.client.post('/api/v1/places/', json={
            "id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": response_user.get_json()['id'] 
        })
        self.assertEqual(response_place.status_code, 201)

        response_review = self.client.post('/api/v1/reviews/', json={
            "id": "2fa85f64-5717-4562-b3fc-2c963f66afa6",
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": response_user.get_json()['id'],
            "place_id": response_place.get_json()['id'] 
        })
        self.assertEqual(response_review.status_code, 201)

    # ------------ GET TESTS ------------

    def test_get_amenity(self):
        response_amenity = self.client.post('/api/v1/amenities/', json={
            "name": "Wi-Fi",
        })
        amenity_id = response_amenity.get_json()['id']
        response_amenity = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response_amenity.status_code, 200)
    
    def test_get_amenity_invalid(self):
        response_amenity = self.client.get('/api/v1/amenities/Fake_amenity_id')
        self.assertEqual(response_amenity.status_code, 404)

    def test_get_user(self):
        response_user = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        user_id = response_amenity.get_json()['id']
        response_user = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response_user.status_code, 200)

    def test_get_user_invalid(self):
        response_user = self.client.get('/api/v1/users/fake-user-id')
        self.assertEqual(response_user.status_code, 404)

    def test_get_place(self):
        response_user = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe4@example.com"
        })
        response_place = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": response_user.get_json()['id']
        })
        place_id = response_place.get_json()['id']
        response_place = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response_place.status_code, 200)

    def test_get_place_invalid(self):
        response_place = self.client.get('/api/v1/places/fake-place-id')
        self.assertEqual(response_place.status_code, 404)

    def test_get_review(self):
        response_user = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith2@example.com"
        })
        response_place = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": response_user.get_json()['id']
        })
        response_review = self.client.post('/api/v1/reviews/', json={
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": response_user.get_json()['id'],
            "place_id": response_place.get_json()['id']
        })
        review_id = response_review.get_json()['id']
        response_review = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response_review.status_code, 200)

    def test_get_review_invalid(self):
        response_review = self.client.get('/api/v1/reviews/fake-review-id')
        self.assertEqual(response_review.status_code, 404)

    # ------------ PUT TESTS ------------

    def test_put_amenity(self):
        response_amenity = self.client.post('/api/v1/amenities/', json={
            "name": "Wi-Fi",
        })
        amenity_id = response_amenity.get_json()['id']
        response_amenity = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            "name": "Air Conditioning",
        })
        self.assertEqual(response_amenity.status_code, 200)

    def test_put_amenity_invalid(self):
        response_amenity = self.client.put('/api/v1/amenities/fake-amenity-id', json={
            "name": "Air Conditioning",
        })
        self.assertEqual(response_amenity.status_code, 404)

    def test_put_user(self):
        response_user = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe5@example.com"
        })
        user_id = response_user.get_json()['id']
        response_user = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe5@example.com"
        })
        self.assertEqual(response_user.status_code, 200)

    def test_put_user_invalid(self):
        response_user = self.client.put('/api/v1/users/fake-user-id', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe6@example.com"
        })
        self.assertEqual(response_user.status_code, 404)

    def test_put_place(self):
        response_user = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe7@example.com"
        })
        response_place = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": response_user.get_json()['id']
        })
        place_id = response_place.get_json()['id']
        response_place = self.client.put(f'/api/v1/places/{place_id}', json={
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
        response_user = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith3@example.com"
        })
        response_place = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": response_user.get_json()['id']
        })
        response_review = self.client.post('/api/v1/reviews/', json={
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": response_user.get_json()['id'],
            "place_id": response_place.get_json()['id']
        })
        review_id = response_review.get_json()['id']
        response_review = self.client.put(f'/api/v1/reviews/{review_id}', json={
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
