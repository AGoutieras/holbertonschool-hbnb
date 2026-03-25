import requests

BASE_URL = "http://localhost:5000/api/v1"
PLACE_ID = "05da39a6-51f8-4b87-8740-0ae26c3fbae5"

# Login admin
admin_token = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "admin@hbnb.io",
    "password": "admin123"
}).json()["access_token"]

# Fake users
users = [
    {"first_name": "Alice", "last_name": "Martin", "email": "alice@test.com", "password": "password123"},
    {"first_name": "Bob", "last_name": "Dupont", "email": "bob@test.com", "password": "password123"},
    {"first_name": "Clara", "last_name": "Bernard", "email": "clara@test.com", "password": "password123"},
    {"first_name": "David", "last_name": "Moreau", "email": "david@test.com", "password": "password123"},
]

reviews = [
    {"text": "Endroit magnifique, je recommande vivement !", "rating": 5},
    {"text": "Très bon séjour, hôte accueillant.", "rating": 4},
    {"text": "Correct pour le prix, rien d'exceptionnel.", "rating": 3},
    {"text": "Super expérience, on reviendra !", "rating": 5},
]

for user, review in zip(users, reviews):
    resp = requests.post(f"{BASE_URL}/users/", json=user, headers={"Authorization": f"Bearer {admin_token}"})
    if resp.status_code not in (200, 201):
        print(f"Erreur création user {user['email']}: {resp.json()}")
        continue
    user_id = resp.json()["id"]

    token = requests.post(f"{BASE_URL}/auth/login", json={
        "email": user["email"], "password": user["password"]
    }).json()["access_token"]

    resp = requests.post(f"{BASE_URL}/reviews/", json={
        "text": review["text"],
        "rating": review["rating"],
        "user_id": user_id,
        "place_id": PLACE_ID
    }, headers={"Authorization": f"Bearer {token}"})

    if resp.status_code == 201:
        print(f"✅ Review postée par {user['first_name']} (rating: {review['rating']})")
    else:
        print(f"❌ Erreur review {user['first_name']}: {resp.json()}")