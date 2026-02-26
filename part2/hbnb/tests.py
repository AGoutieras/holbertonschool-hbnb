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





    # ------------ PUT TESTS ------------




    