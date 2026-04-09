#!/bin/bash

# Colors
RED="\033[31m"
GREEN="\e[0;92m"
YELLOW="\033[33m"
BLUE="\033[34m"
MAGENTA="\033[35m"
CYAN="\033[36m"
ORANGE="\033[38;5;208m"
PINK="\033[38;5;213m"
LIME="\033[38;5;154m"
TEAL="\033[38;5;51m"
PURPLE="\033[38;5;141m"
GRAY="\033[38;5;245m"
WHITE="\e[0;97m"
RESET="\033[0m"

SEPARATOR="${WHITE}----------------------------------------${RESET}"

TIMESTAMP=$(date +%s)
EMAIL1="john.doe.$TIMESTAMP@example.com"
EMAIL2="jane.doe.$TIMESTAMP@example.com"

# Clean database
sqlite3 instance/development.db "DELETE FROM reviews; DELETE FROM places; DELETE FROM users WHERE email != 'admin@hbnb.io';"
echo -e "${PINK}Database cleaned!${RESET}"

echo -e "\n${WHITE}========== SETUP ==========${RESET}"

# Login with Admin
ADMINTOKEN=$(curl -s -X POST "http://localhost:5000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@hbnb.io", "password": "admin123"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
echo -e "$SEPARATOR"
echo -e "${RED}Admin token: $ADMINTOKEN${RESET}"

# Create first user
USER1=$(curl -s -X POST "http://localhost:5000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMINTOKEN" \
  -d "{\"first_name\": \"John\", \"last_name\": \"Doe\", \"email\": \"$EMAIL1\", \"password\": \"password\"}" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo -e "$SEPARATOR"
echo -e "${GREEN}First User ID: $USER1${RESET}"

# Login with first user
TOKEN1=$(curl -s -X POST "http://localhost:5000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL1\", \"password\": \"password\"}" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
echo -e "$SEPARATOR"
echo -e "${GREEN}First User Token: $TOKEN1${RESET}"

# Create second user
USER2=$(curl -s -X POST "http://localhost:5000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMINTOKEN" \
  -d "{\"first_name\": \"Jane\", \"last_name\": \"Doe\", \"email\": \"$EMAIL2\", \"password\": \"password\"}" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo -e "$SEPARATOR"
echo -e "${BLUE}Second User ID: $USER2${RESET}"

# Login with second user
TOKEN2=$(curl -s -X POST "http://localhost:5000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL2\", \"password\": \"password\"}" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
echo -e "$SEPARATOR"
echo -e "${BLUE}Second User Token: $TOKEN2${RESET}"

# Create a place
PLACE=$(curl -s -X POST "http://localhost:5000/api/v1/places/" \
  -H "Authorization: Bearer $TOKEN1" \
  -H "Content-Type: application/json" \
  -d '{"title": "Appartement", "description": "test", "price": 100.0, "latitude": 25.0, "longitude": 25.0, "amenities": []}' | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo -e "$SEPARATOR"
echo -e "${YELLOW}Place ID: $PLACE${RESET}"

# Create a review (user2 reviews user1's place) -> should succeed
REVIEW_ID=$(curl -s -X POST "http://localhost:5000/api/v1/reviews/" \
  -H "Authorization: Bearer $TOKEN2" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Great place to stay!\", \"rating\": 5, \"user_id\": \"$USER2\", \"place_id\": \"$PLACE\"}" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo -e "$SEPARATOR"
echo -e "${MAGENTA}Review ID: $REVIEW_ID${RESET}"


echo -e "\n${WHITE}========== PUBLIC ENDPOINTS (no token) ==========${RESET}"

# GET all places -> should succeed
echo -e "$SEPARATOR"
echo -e "${TEAL}[GET /places/] - should return list:${RESET}"
curl -s -X GET "http://localhost:5000/api/v1/places/" | python3 -c "import sys,json; data=json.load(sys.stdin); print(f'  -> {len(data)} place(s) found')"

# GET one place -> should succeed
echo -e "$SEPARATOR"
echo -e "${TEAL}[GET /places/<id>] - should return place details:${RESET}"
curl -s -X GET "http://localhost:5000/api/v1/places/$PLACE" | python3 -c "import sys,json; data=json.load(sys.stdin); print(f'  -> title: {data.get(\"title\", \"ERROR\")}')"


echo -e "\n${WHITE}========== PLACE OWNERSHIP ==========${RESET}"

# PUT place as owner -> should succeed
echo -e "$SEPARATOR"
echo -e "${LIME}[PUT /places/<id>] as owner (user1) - should succeed:${RESET}"
curl -s -X PUT "http://localhost:5000/api/v1/places/$PLACE" \
  -H "Authorization: Bearer $TOKEN1" \
  -H "Content-Type: application/json" \
  -d '{"title": "Appartement Updated", "description": "updated", "price": 120.0, "latitude": 25.0, "longitude": 25.0}' | python3 -c "import sys,json; data=json.load(sys.stdin); print(f'  -> {data}')"

# PUT place as non-owner -> should fail with 403
echo -e "$SEPARATOR"
echo -e "${ORANGE}[PUT /places/<id>] as non-owner (user2) - should return 403:${RESET}"
curl -s -X PUT "http://localhost:5000/api/v1/places/$PLACE" \
  -H "Authorization: Bearer $TOKEN2" \
  -H "Content-Type: application/json" \
  -d '{"title": "Hacked!", "description": "hacked", "price": 1.0, "latitude": 25.0, "longitude": 25.0}' | python3 -c "import sys,json; data=json.load(sys.stdin); print(f'  -> {data}')"


echo -e "\n${WHITE}========== REVIEW RESTRICTIONS ==========${RESET}"

# POST review on own place -> should fail with 400
echo -e "$SEPARATOR"
echo -e "${ORANGE}[POST /reviews/] owner reviewing own place - should return 400:${RESET}"
curl -s -X POST "http://localhost:5000/api/v1/reviews/" \
  -H "Authorization: Bearer $TOKEN1" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"My own place is great!\", \"rating\": 5, \"user_id\": \"$USER1\", \"place_id\": \"$PLACE\"}" | python3 -c "import sys,json; data=json.load(sys.stdin); print(f'  -> {data}')"

# POST duplicate review -> should fail with 400
echo -e "$SEPARATOR"
echo -e "${ORANGE}[POST /reviews/] duplicate review (user2) - should return 400:${RESET}"
curl -s -X POST "http://localhost:5000/api/v1/reviews/" \
  -H "Authorization: Bearer $TOKEN2" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Again!\", \"rating\": 3, \"user_id\": \"$USER2\", \"place_id\": \"$PLACE\"}" | python3 -c "import sys,json; data=json.load(sys.stdin); print(f'  -> {data}')"

# PUT review as author -> should succeed
echo -e "$SEPARATOR"
echo -e "${LIME}[PUT /reviews/<id>] as author (user2) - should succeed:${RESET}"
curl -s -X PUT "http://localhost:5000/api/v1/reviews/$REVIEW_ID" \
  -H "Authorization: Bearer $TOKEN2" \
  -H "Content-Type: application/json" \
  -d '{"text": "Updated review!", "rating": 4}' | python3 -c "import sys,json; data=json.load(sys.stdin); print(f'  -> {data}')"

# PUT review as non-author -> should fail with 403
echo -e "$SEPARATOR"
echo -e "${ORANGE}[PUT /reviews/<id>] as non-author (user1) - should return 403:${RESET}"
curl -s -X PUT "http://localhost:5000/api/v1/reviews/$REVIEW_ID" \
  -H "Authorization: Bearer $TOKEN1" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hacked review!", "rating": 1}' | python3 -c "import sys,json; data=json.load(sys.stdin); print(f'  -> {data}')"

# DELETE review as non-author -> should fail with 403
echo -e "$SEPARATOR"
echo -e "${ORANGE}[DELETE /reviews/<id>] as non-author (user1) - should return 403:${RESET}"
curl -s -X DELETE "http://localhost:5000/api/v1/reviews/$REVIEW_ID" \
  -H "Authorization: Bearer $TOKEN1" | python3 -c "import sys,json; data=json.load(sys.stdin); print(f'  -> {data}')"

# DELETE review as author -> should succeed
echo -e "$SEPARATOR"
echo -e "${LIME}[DELETE /reviews/<id>] as author (user2) - should succeed:${RESET}"
curl -s -X DELETE "http://localhost:5000/api/v1/reviews/$REVIEW_ID" \
  -H "Authorization: Bearer $TOKEN2" | python3 -c "import sys,json; data=json.load(sys.stdin); print(f'  -> {data}')"


echo -e "\n${WHITE}========== USER SELF-MODIFICATION ==========${RESET}"

# PUT own user data -> should succeed
echo -e "$SEPARATOR"
echo -e "${LIME}[PUT /users/<id>] modify own data - should succeed:${RESET}"
curl -s -X PUT "http://localhost:5000/api/v1/users/$USER1" \
  -H "Authorization: Bearer $TOKEN1" \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Johnny"}' | python3 -c "import sys,json; data=json.load(sys.stdin); print(f'  -> {data}')"

# PUT own email -> should fail with 400
echo -e "$SEPARATOR"
echo -e "${ORANGE}[PUT /users/<id>] modify own email - should return 400:${RESET}"
curl -s -X PUT "http://localhost:5000/api/v1/users/$USER1" \
  -H "Authorization: Bearer $TOKEN1" \
  -H "Content-Type: application/json" \
  -d '{"email": "newemail@example.com"}' | python3 -c "import sys,json; data=json.load(sys.stdin); print(f'  -> {data}')"

# PUT another user's data -> should fail with 403
echo -e "$SEPARATOR"
echo -e "${ORANGE}[PUT /users/<id>] modify other user's data - should return 403:${RESET}"
curl -s -X PUT "http://localhost:5000/api/v1/users/$USER2" \
  -H "Authorization: Bearer $TOKEN1" \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Hacked"}' | python3 -c "import sys,json; data=json.load(sys.stdin); print(f'  -> {data}')"


echo -e "\n${WHITE}========== ADMIN PRIVILEGES ==========${RESET}"

# Admin creates amenity -> should succeed
echo -e "$SEPARATOR"
echo -e "${PURPLE}[POST /amenities/] as admin - should succeed:${RESET}"
AMENITY=$(curl -s -X POST "http://localhost:5000/api/v1/amenities/" \
  -H "Authorization: Bearer $ADMINTOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "WiFi"}' | python3 -c "import sys,json; data=json.load(sys.stdin); print(data.get('id', data))")
echo -e "  -> Amenity ID: $AMENITY"

# Non-admin creates amenity -> should fail with 403
echo -e "$SEPARATOR"
echo -e "${ORANGE}[POST /amenities/] as non-admin - should return 403:${RESET}"
curl -s -X POST "http://localhost:5000/api/v1/amenities/" \
  -H "Authorization: Bearer $TOKEN1" \
  -H "Content-Type: application/json" \
  -d '{"name": "Pool"}' | python3 -c "import sys,json; data=json.load(sys.stdin); print(f'  -> {data}')"

# Admin modifies any place -> should succeed (bypass ownership)
echo -e "$SEPARATOR"
echo -e "${PURPLE}[PUT /places/<id>] as admin (not owner) - should succeed:${RESET}"
curl -s -X PUT "http://localhost:5000/api/v1/places/$PLACE" \
  -H "Authorization: Bearer $ADMINTOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Admin Updated", "description": "admin edit", "price": 999.0, "latitude": 25.0, "longitude": 25.0}' | python3 -c "import sys,json; data=json.load(sys.stdin); print(f'  -> {data}')"

echo -e "\n${LIME}========== TESTS DONE ==========${RESET}\n"