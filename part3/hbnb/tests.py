import unittest
from app import create_app, db


def clean_db(app):
    with app.app_context():
        db.session.execute(db.text("DELETE FROM reviews"))
        db.session.execute(db.text("DELETE FROM place_amenity"))
        db.session.execute(db.text("DELETE FROM places"))
        db.session.execute(db.text("DELETE FROM amenities"))
        db.session.execute(
            db.text("DELETE FROM users WHERE email != 'admin@hbnb.io'"))
        db.session.commit()


class BaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.app.config["TESTING"] = True

    def setUp(self):
        clean_db(self.app)
        self.admin_token = self._login("admin@hbnb.io", "admin123")

    def _login(self, email, password):
        resp = self.client.post("/api/v1/auth/login", json={
            "email": email,
            "password": password
        })
        return resp.get_json().get("access_token", "")

    def _auth(self, token):
        return {"Authorization": f"Bearer {token}"}

    def _create_user(self, email, first_name="Test", last_name="User", password="password"):
        resp = self.client.post("/api/v1/users/", json={
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        }, headers=self._auth(self.admin_token))
        return resp.get_json().get("id"), self._login(email, password)

    def _create_amenity(self, name="WiFi"):
        resp = self.client.post("/api/v1/amenities/", json={
            "name": name
        }, headers=self._auth(self.admin_token))
        return resp.get_json().get("id")

    def _create_place(self, token, title="Test Place", amenities=None):
        resp = self.client.post("/api/v1/places/", json={
            "title": title,
            "description": "Test description",
            "price": 100.0,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "amenities": amenities or []
        }, headers=self._auth(token))
        return resp.get_json().get("id")

    def _create_review(self, token, place_id, user_id, text="Great!", rating=5):
        resp = self.client.post("/api/v1/reviews/", json={
            "text": text,
            "rating": rating,
            "user_id": user_id,
            "place_id": place_id
        }, headers=self._auth(token))
        return resp.get_json().get("id"), resp.status_code


class TestAuthentication(BaseTestCase):

    def test_admin_login_success(self):
        resp = self.client.post("/api/v1/auth/login", json={
            "email": "admin@hbnb.io",
            "password": "admin123"
        })
        self.assertEqual(resp.status_code, 200)
        self.assertIn("access_token", resp.get_json())

    def test_login_wrong_password(self):
        resp = self.client.post("/api/v1/auth/login", json={
            "email": "admin@hbnb.io",
            "password": "wrongpassword"
        })
        self.assertEqual(resp.status_code, 401)
        self.assertIn("error", resp.get_json())

    def test_login_nonexistent_email(self):
        resp = self.client.post("/api/v1/auth/login", json={
            "email": "nobody@example.com",
            "password": "password"
        })
        self.assertEqual(resp.status_code, 401)

    def test_post_users_without_token(self):
        resp = self.client.post("/api/v1/users/", json={
            "first_name": "T", "last_name": "T",
            "email": "t@t.com", "password": "t"
        })
        self.assertEqual(resp.status_code, 401)

    def test_post_places_without_token(self):
        resp = self.client.post("/api/v1/places/", json={
            "title": "T", "price": 10,
            "latitude": 0, "longitude": 0, "amenities": []
        })
        self.assertEqual(resp.status_code, 401)

    def test_post_reviews_without_token(self):
        resp = self.client.post("/api/v1/reviews/", json={
            "text": "T", "rating": 3,
            "user_id": "x", "place_id": "x"
        })
        self.assertEqual(resp.status_code, 401)


class TestAdminUserManagement(BaseTestCase):

    def test_admin_creates_user(self):
        resp = self.client.post("/api/v1/users/", json={
            "first_name": "John", "last_name": "Doe",
            "email": "john@test.com", "password": "password"
        }, headers=self._auth(self.admin_token))
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertIn("id", data)
        self.assertNotIn("password", data)

    def test_admin_creates_user_duplicate_email(self):
        self.client.post("/api/v1/users/", json={
            "first_name": "John", "last_name": "Doe",
            "email": "john@test.com", "password": "password"
        }, headers=self._auth(self.admin_token))
        resp = self.client.post("/api/v1/users/", json={
            "first_name": "Dup", "last_name": "Dup",
            "email": "john@test.com", "password": "password"
        }, headers=self._auth(self.admin_token))
        self.assertEqual(resp.status_code, 400)
        self.assertIn("error", resp.get_json())

    def test_non_admin_cannot_create_user(self):
        user_id, token = self._create_user("user@test.com")
        resp = self.client.post("/api/v1/users/", json={
            "first_name": "Hack", "last_name": "Hack",
            "email": "hack@test.com", "password": "password"
        }, headers=self._auth(token))
        self.assertEqual(resp.status_code, 403)

    def test_admin_updates_user_email(self):
        user_id, _ = self._create_user("user@test.com")
        resp = self.client.put(f"/api/v1/users/{user_id}", json={
            "email": "updated@test.com"
        }, headers=self._auth(self.admin_token))
        self.assertEqual(resp.status_code, 200)

    def test_admin_cannot_set_duplicate_email(self):
        user1_id, _ = self._create_user("user1@test.com")
        user2_id, _ = self._create_user("user2@test.com")
        resp = self.client.put(f"/api/v1/users/{user1_id}", json={
            "email": "user2@test.com"
        }, headers=self._auth(self.admin_token))
        self.assertEqual(resp.status_code, 400)


class TestUserCRUD(BaseTestCase):

    def test_get_all_users_public(self):
        resp = self.client.get("/api/v1/users/")
        self.assertEqual(resp.status_code, 200)

    def test_get_user_by_id(self):
        user_id, _ = self._create_user("user@test.com")
        resp = self.client.get(f"/api/v1/users/{user_id}")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("first_name", data)
        self.assertIn("email", data)
        self.assertNotIn("password", data)

    def test_get_user_invalid_id(self):
        resp = self.client.get("/api/v1/users/fake-id-that-doesnt-exist")
        self.assertEqual(resp.status_code, 404)

    def test_user_updates_own_first_name(self):
        user_id, token = self._create_user("user@test.com", first_name="John")
        resp = self.client.put(f"/api/v1/users/{user_id}", json={
            "first_name": "Johnny"
        }, headers=self._auth(token))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["first_name"], "Johnny")

    def test_user_cannot_update_own_email(self):
        user_id, token = self._create_user("user@test.com")
        resp = self.client.put(f"/api/v1/users/{user_id}", json={
            "email": "newemail@test.com"
        }, headers=self._auth(token))
        self.assertEqual(resp.status_code, 400)

    def test_user_cannot_update_own_password(self):
        user_id, token = self._create_user("user@test.com")
        resp = self.client.put(f"/api/v1/users/{user_id}", json={
            "password": "newpassword"
        }, headers=self._auth(token))
        self.assertEqual(resp.status_code, 400)

    def test_user_cannot_update_another_user(self):
        user1_id, token1 = self._create_user("user1@test.com")
        user2_id, token2 = self._create_user("user2@test.com")
        resp = self.client.put(f"/api/v1/users/{user2_id}", json={
            "first_name": "Hacked"
        }, headers=self._auth(token1))
        self.assertEqual(resp.status_code, 403)

    def test_put_user_invalid_id(self):
        _, token = self._create_user("user@test.com")
        resp = self.client.put("/api/v1/users/fake-id", json={
            "first_name": "Test"
        }, headers=self._auth(token))
        self.assertEqual(resp.status_code, 404)


class TestAmenityManagement(BaseTestCase):

    def test_admin_creates_amenity(self):
        resp = self.client.post("/api/v1/amenities/", json={
            "name": "WiFi"
        }, headers=self._auth(self.admin_token))
        self.assertEqual(resp.status_code, 201)
        self.assertIn("id", resp.get_json())

    def test_non_admin_cannot_create_amenity(self):
        _, token = self._create_user("user@test.com")
        resp = self.client.post("/api/v1/amenities/", json={
            "name": "Sauna"
        }, headers=self._auth(token))
        self.assertEqual(resp.status_code, 403)

    def test_get_all_amenities_public(self):
        resp = self.client.get("/api/v1/amenities/")
        self.assertEqual(resp.status_code, 200)

    def test_get_amenity_by_id(self):
        amenity_id = self._create_amenity("WiFi")
        resp = self.client.get(f"/api/v1/amenities/{amenity_id}")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("name", resp.get_json())

    def test_get_amenity_invalid_id(self):
        resp = self.client.get("/api/v1/amenities/fake-id")
        self.assertEqual(resp.status_code, 404)

    def test_admin_updates_amenity(self):
        amenity_id = self._create_amenity("WiFi")
        resp = self.client.put(f"/api/v1/amenities/{amenity_id}", json={
            "name": "WiFi Updated"
        }, headers=self._auth(self.admin_token))
        self.assertEqual(resp.status_code, 200)

    def test_non_admin_cannot_update_amenity(self):
        amenity_id = self._create_amenity("WiFi")
        _, token = self._create_user("user@test.com")
        resp = self.client.put(f"/api/v1/amenities/{amenity_id}", json={
            "name": "Hacked"
        }, headers=self._auth(token))
        self.assertEqual(resp.status_code, 403)

    def test_put_amenity_invalid_id(self):
        resp = self.client.put("/api/v1/amenities/fake-id", json={
            "name": "Test"
        }, headers=self._auth(self.admin_token))
        self.assertEqual(resp.status_code, 404)


class TestPlaceManagement(BaseTestCase):

    def test_user_creates_place_with_amenity(self):
        _, token = self._create_user("user@test.com")
        amenity_id = self._create_amenity("WiFi")
        resp = self.client.post("/api/v1/places/", json={
            "title": "Test Place",
            "description": "Nice",
            "price": 100.0,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "amenities": [amenity_id]
        }, headers=self._auth(token))
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertIn("id", data)
        self.assertIn("owner_id", data)

    def test_create_place_negative_price(self):
        _, token = self._create_user("user@test.com")
        resp = self.client.post("/api/v1/places/", json={
            "title": "Bad", "description": "Bad",
            "price": -50.0, "latitude": 0.0,
            "longitude": 0.0, "amenities": []
        }, headers=self._auth(token))
        self.assertEqual(resp.status_code, 400)

    def test_create_place_invalid_amenity(self):
        _, token = self._create_user("user@test.com")
        resp = self.client.post("/api/v1/places/", json={
            "title": "Bad", "description": "Bad",
            "price": 100.0, "latitude": 0.0,
            "longitude": 0.0, "amenities": ["fake-amenity-id"]
        }, headers=self._auth(token))
        self.assertEqual(resp.status_code, 400)

    def test_get_all_places_public(self):
        resp = self.client.get("/api/v1/places/")
        self.assertEqual(resp.status_code, 200)

    def test_get_place_by_id_public(self):
        _, token = self._create_user("user@test.com")
        place_id = self._create_place(token)
        resp = self.client.get(f"/api/v1/places/{place_id}")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("owner", data)
        self.assertIn("amenities", data)

    def test_get_place_invalid_id(self):
        resp = self.client.get("/api/v1/places/fake-id")
        self.assertEqual(resp.status_code, 404)

    def test_get_place_reviews_public(self):
        _, token = self._create_user("user@test.com")
        place_id = self._create_place(token)
        resp = self.client.get(f"/api/v1/places/{place_id}/reviews")
        self.assertEqual(resp.status_code, 200)

    def test_get_reviews_invalid_place(self):
        resp = self.client.get("/api/v1/places/fake-id/reviews")
        self.assertEqual(resp.status_code, 404)

    def test_owner_updates_own_place(self):
        _, token = self._create_user("user@test.com")
        place_id = self._create_place(token)
        resp = self.client.put(f"/api/v1/places/{place_id}", json={
            "title": "Updated", "description": "Updated",
            "price": 120.0, "latitude": 48.8566,
            "longitude": 2.3522, "amenities": []
        }, headers=self._auth(token))
        self.assertEqual(resp.status_code, 200)

    def test_non_owner_cannot_update_place(self):
        _, token1 = self._create_user("user1@test.com")
        _, token2 = self._create_user("user2@test.com")
        place_id = self._create_place(token1)
        resp = self.client.put(f"/api/v1/places/{place_id}", json={
            "title": "Hacked", "description": "Bad",
            "price": 1.0, "latitude": 0.0,
            "longitude": 0.0, "amenities": []
        }, headers=self._auth(token2))
        self.assertEqual(resp.status_code, 403)

    def test_put_place_invalid_id(self):
        _, token = self._create_user("user@test.com")
        resp = self.client.put("/api/v1/places/fake-id", json={
            "title": "T", "description": "T",
            "price": 100.0, "latitude": 0.0,
            "longitude": 0.0, "amenities": []
        }, headers=self._auth(token))
        self.assertEqual(resp.status_code, 404)

    def test_admin_bypasses_place_ownership(self):
        _, token = self._create_user("user@test.com")
        place_id = self._create_place(token)
        resp = self.client.put(f"/api/v1/places/{place_id}", json={
            "title": "Admin Override", "description": "Admin",
            "price": 999.0, "latitude": 0.0,
            "longitude": 0.0, "amenities": []
        }, headers=self._auth(self.admin_token))
        self.assertEqual(resp.status_code, 200)


class TestReviewManagement(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.user1_id, self.token1 = self._create_user("user1@test.com")
        self.user2_id, self.token2 = self._create_user("user2@test.com")
        self.place1_id = self._create_place(self.token1, title="Place 1")
        self.place2_id = self._create_place(self.token2, title="Place 2")

    def test_user_reviews_another_users_place(self):
        review_id, status = self._create_review(
            self.token2, self.place1_id, self.user2_id
        )
        self.assertEqual(status, 201)
        self.assertIsNotNone(review_id)

    def test_owner_cannot_review_own_place(self):
        _, status = self._create_review(
            self.token1, self.place1_id, self.user1_id
        )
        self.assertEqual(status, 400)

    def test_user_cannot_review_same_place_twice(self):
        self._create_review(self.token2, self.place1_id, self.user2_id)
        _, status = self._create_review(
            self.token2, self.place1_id, self.user2_id, text="Again!"
        )
        self.assertEqual(status, 400)

    def test_review_invalid_place_id(self):
        _, status = self._create_review(
            self.token2, "fake-place-id", self.user2_id
        )
        self.assertEqual(status, 404)

    def test_get_all_reviews(self):
        resp = self.client.get("/api/v1/reviews/")
        self.assertEqual(resp.status_code, 200)

    def test_get_review_by_id(self):
        review_id, _ = self._create_review(
            self.token2, self.place1_id, self.user2_id
        )
        resp = self.client.get(f"/api/v1/reviews/{review_id}")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("text", data)
        self.assertIn("rating", data)

    def test_get_review_invalid_id(self):
        resp = self.client.get("/api/v1/reviews/fake-id")
        self.assertEqual(resp.status_code, 404)

    def test_get_reviews_for_place(self):
        self._create_review(self.token2, self.place1_id, self.user2_id)
        resp = self.client.get(f"/api/v1/places/{self.place1_id}/reviews")
        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(len(resp.get_json()), 1)

    def test_author_updates_own_review(self):
        review_id, _ = self._create_review(
            self.token2, self.place1_id, self.user2_id
        )
        resp = self.client.put(f"/api/v1/reviews/{review_id}", json={
            "text": "Updated!", "rating": 4,
            "user_id": "x", "place_id": "x"
        }, headers=self._auth(self.token2))
        self.assertEqual(resp.status_code, 200)

    def test_non_author_cannot_update_review(self):
        review_id, _ = self._create_review(
            self.token2, self.place1_id, self.user2_id
        )
        resp = self.client.put(f"/api/v1/reviews/{review_id}", json={
            "text": "Hacked!", "rating": 1,
            "user_id": "x", "place_id": "x"
        }, headers=self._auth(self.token1))
        self.assertEqual(resp.status_code, 403)

    def test_put_review_invalid_id(self):
        resp = self.client.put("/api/v1/reviews/fake-id", json={
            "text": "T", "rating": 3,
            "user_id": "x", "place_id": "x"
        }, headers=self._auth(self.token2))
        self.assertEqual(resp.status_code, 404)

    def test_non_author_cannot_delete_review(self):
        review_id, _ = self._create_review(
            self.token2, self.place1_id, self.user2_id
        )
        resp = self.client.delete(
            f"/api/v1/reviews/{review_id}",
            headers=self._auth(self.token1)
        )
        self.assertEqual(resp.status_code, 403)

    def test_delete_review_invalid_id(self):
        resp = self.client.delete(
            "/api/v1/reviews/fake-id",
            headers=self._auth(self.token2)
        )
        self.assertEqual(resp.status_code, 404)

    def test_author_deletes_own_review(self):
        review_id, _ = self._create_review(
            self.token2, self.place1_id, self.user2_id
        )
        resp = self.client.delete(
            f"/api/v1/reviews/{review_id}",
            headers=self._auth(self.token2)
        )
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(f"/api/v1/reviews/{review_id}")
        self.assertEqual(resp.status_code, 404)

    def test_admin_updates_any_review(self):
        review_id, _ = self._create_review(
            self.token2, self.place1_id, self.user2_id
        )
        resp = self.client.put(f"/api/v1/reviews/{review_id}", json={
            "text": "Admin edit", "rating": 3,
            "user_id": "x", "place_id": "x"
        }, headers=self._auth(self.admin_token))
        self.assertEqual(resp.status_code, 200)

    def test_admin_deletes_any_review(self):
        review_id, _ = self._create_review(
            self.token2, self.place1_id, self.user2_id
        )
        resp = self.client.delete(
            f"/api/v1/reviews/{review_id}",
            headers=self._auth(self.admin_token)
        )
        self.assertEqual(resp.status_code, 200)


if __name__ == "__main__":
    unittest.main(verbosity=2)
