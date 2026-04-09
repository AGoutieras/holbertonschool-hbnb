#!/bin/bash

# Colors
RED="\033[31m"
GREEN="\e[0;92m"
YELLOW="\033[33m"
BLUE="\033[34m"
MAGENTA="\033[35m"
CYAN="\033[36m"
WHITE="\e[0;97m"
RESET="\033[0m"

# Login with Admin
ADMINTOKEN=$(curl -s -X POST "http://localhost:5000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@hbnb.io", "password": "admin123"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
echo -e "${WHITE}----------------------------------------${RESET}"
echo -e "${RED}Admin token: $ADMINTOKEN${RESET}"


# Create first user
USER1=$(curl -s -X POST "http://localhost:5000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMINTOKEN" \
  -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com", "password": "password"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo -e "${WHITE}----------------------------------------${RESET}"
echo -e "${GREEN}First User ID: $USER1${RESET}"

# Login with first user
TOKEN1=$(curl -s -X POST "http://localhost:5000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "john.doe@example.com", "password": "password"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
echo -e "${WHITE}----------------------------------------${RESET}"
echo -e "${GREEN}First User Token: $TOKEN1${RESET}"

# Create second user
USER2=$(curl -s -X POST "http://localhost:5000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMINTOKEN" \
  -d '{"first_name": "Jane", "last_name": "Doe", "email": "jane.doe@example.com", "password": "password"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo -e "${WHITE}----------------------------------------${RESET}"
echo -e "${BLUE}Second User ID: $USER2${RESET}"

# Login with second user
TOKEN2=$(curl -s -X POST "http://localhost:5000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "jane.doe@example.com", "password": "password"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
echo -e "${WHITE}----------------------------------------${RESET}"
echo -e "${BLUE}Second User Token: $TOKEN2${RESET}"

# Create a place
PLACE=$(curl -s -X POST "http://localhost:5000/api/v1/places/" \
  -H "Authorization: Bearer $TOKEN1" \
  -H "Content-Type: application/json" \
  -d '{"title": "Appartement", "description": "test", "price": 100.0, "latitude": 25.0, "longitude": 25.0, "amenities": []}' | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo -e "${WHITE}----------------------------------------${RESET}"
echo -e "${YELLOW}Place ID: $PLACE${RESET}"

# Create a review
REVIEW=$(curl -s -X POST "http://localhost:5000/api/v1/reviews/" \
  -H "Authorization: Bearer $TOKEN2" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Great place to stay!\", \"rating\": 5, \"user_id\": \"$USER2\", \"place_id\": \"$PLACE\"}")
echo -e "${WHITE}----------------------------------------${RESET}"
echo -e "${MAGENTA}Review: $REVIEW${RESET}"

# Create an amenity
AMENITY=$(curl -s -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMINTOKEN" \
  -d '{"name": "Wi-Fi"}')
echo -e "${WHITE}----------------------------------------${RESET}"
echo -e "${CYAN}Amenity: $AMENITY${RESET}"