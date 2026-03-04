<a href="#"><img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue"/></a>
<a href="#"><img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white"/></a>
[![Holberton](https://img.shields.io/badge/Holberton-E31C3F.svg?style=for-the-badge)](https://www.holbertonschool.fr/)

# HbnB Part 2: Business Logic and API Endpoints

This is the second part of the **HbnB** project, the AirBnB clone.
In this part, we focus on implementing the **Business Logic**, the `REST API`, and the necessary endpoints for *Users*, *Amenities*, *Places*, and *Reviews*.

## Table of Contents
1. [File Structure](#file-structure)
2. [Requirements](#requirements)
3. [Starting the application](#starting-the-application)
4. [API Usage](#api-usage)
5. [Authors](#authors)

## File Structure

```text
	hbnb/
	├── app/
	│   ├── __init__.py
	│   ├── api/
	│   │   ├── __init__.py
	│   │   ├── v1/
	│   │       ├── __init__.py
	│   │       ├── amenities.py
	│   │       ├── places.py
	│   │       ├── reviews.py
	│   │       ├── users.py
	│   ├── models/
	│   │   ├── __init__.py
	│   │   ├── amenity.py
	│   │   ├── place.py
	│   │   ├── review.py
	│   │   ├── user.py
	│   ├── persistence/
	│   │   ├── __init__.py
	│   │   ├── repository.py
	│   ├── services/
	│   │   ├── __init__.py
	│       ├── facade.py
	├── README.md
	├── config.py 
	├── requirements.txt 
	├── run.py
	├── tests.py
```

**Explanations:**

- The `app/` directory contains the core application code.

- The `api/` subdirectory houses the API endpoints, organized by version (`v1/`).

- The `models/` subdirectory contains the business logic classes (e.g., `user.py`, `place.py`).

- The `persistence/` subdirectory is where the in-memory repository is implemented.
This will later be replaced by a database-backed solution using SQL Alchemy.

- The `services/` subdirectory is where the Facade pattern is implemented, managing the interaction between layers.

- `README.md` will contain a brief overview of the project.

- `config.py` will be used for configuring environment variables and application settings.

- `requirements.txt` will list all the Python packages needed for the project.

- `run.py` is the entry point for running the Flask application.

- `tests.py` is the unit testing file to validate endpoints

## Requirements

To run the HbnB application, you need to install `Flask` and `Flask-RESTX` packages.

```bash
pip install -r requirements.txt
```

## Starting the application

You can start the application using the following command:

```bash
python3 run.py
```

## API Usage

Once the application is running, the following API endpoints are available:

### `User` creation

We can create a new `user` using the `POST` endpoint

```bash
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}'
```

* Expected output:

```json
{
    "id": "7e2c744b-93a3-44f0-9831-16d88acbbcd3",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
}
```

### `Amenity` creation

We can also create a new `amenity`

```bash
curl -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi"}'
```

* Expected output:

```json
{
    "id": "602a65eb-d7a2-4dc8-8fbd-56437b0bfd9f",
    "name": "Wi-Fi"
}
```

### `Place` creation

We can now create a new `place` using `user id` we just created as `owner` alongside the new `amenity`

```bash
curl -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Cozy Apartment", "description": "A nice place to stay", "price": 100.0, "latitude": 37.7749, "longitude": -122.4194, "owner_id": "<owner_id>", "amenities": ["<amenity_id>"]}'
```

* Expected output:

```json
{
    "id": "86610800-61c9-4b32-b3ca-a6eaeaf24a77",
    "title": "Cozy Apartment",
    "description": "A nice place to stay",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "7e2c744b-93a3-44f0-9831-16d88acbbcd3"
}
```

### `Review` creation

We can also create a review for the newly created place

```bash
curl -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Great place to stay!", "rating": 5, "user_id": "<user_id>", "place_id": "<place_id>"}'
  ```

* Expected output:

```json
{
    "id": "6dbd7e6a-8dbc-429f-b534-faa75b8a5307",
    "text": "Great place to stay!",
    "rating": 5,
    "user_id": "7e2c744b-93a3-44f0-9831-16d88acbbcd3",
    "place_id": "86610800-61c9-4b32-b3ca-a6eaeaf24a77"
}
```

### Retrieval of a `User` by ID

We can find a `User`'s details using the `GET` endpoint

```bash
curl -X GET http://localhost:5000/api/v1/users/<user_id>
```

* Expected output:

```json
{
    "id": "7e2c744b-93a3-44f0-9831-16d88acbbcd3",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
}
```

### Retrieval of an `Amenity`'s details

We can retrieve an `amenity`'s details by its ID

```bash
curl -X GET http://localhost:5000/api/v1/amenities/<amenity_id>
```

* Expected output:

```json
{
    "id": "602a65eb-d7a2-4dc8-8fbd-56437b0bfd9f",
    "name": "Wi-Fi"
}
```

### Retrieval of a `Place` details

We can retrieve a `place`'s details, including its `owner` and `amenities`

```bash
curl -X GET http://localhost:5000/api/v1/places/<place_id>
```

* Expected output:

```json
{
    "id": "86610800-61c9-4b32-b3ca-a6eaeaf24a77",
    "title": "Cozy Apartment",
    "description": "A nice place to stay",
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner": {
        "id": "7e2c744b-93a3-44f0-9831-16d88acbbcd3",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    },
    "amenities": [
        {
            "id": "602a65eb-d7a2-4dc8-8fbd-56437b0bfd9f",
            "name": "Wi-Fi"
        }
    ]
}
```

### Updating a `User`

We can update a `user` using the `PUT` endpoint

```bash
curl -X PUT http://localhost:5000/api/v1/users/<user_id> \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Jane", "last_name": "Doe", "email": "jane.doe@example.com"}'
```

* Expected output:

```json
{
    "id": "7e2c744b-93a3-44f0-9831-16d88acbbcd3",
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane.doe@example.com"
}
```

### Updating an `Amenity`

We can change an `amenity`'s information too

```bash
curl -X PUT http://localhost:5000/api/v1/amenities/<amenity_id> \
  -H "Content-Type: application/json" \
  -d '{"name": "Air Conditioning"}'
```

* Expected output:

```json
{
    "message": "Amenity updated successfully"
}
```

### Updating a `Place`'s information

We can update a place's information using its ID

```bash
curl -X PUT http://localhost:5000/api/v1/places/<place_id> \
  -H "Content-Type: application/json" \
  -d '{"title": "Luxury Condo", "description": "An upscale place to stay", "price": 200.0}'
```

* Expected output:

```json
{
    "message": "Place updated successfully"
}
```

### Updating a `Review`

We can also modify an existing review's content and rating

```bash
curl -X PUT http://localhost:5000/api/v1/reviews/<review_id> \
  -H "Content-Type: application/json" \
  -d '{"text": "Amazing stay!", "rating": 4}'
```

* Expected output:

```json
{
    "message": "Review updated successfully"
}
```

### Deleting a `Review`

We can delete a `review` using the `DELETE` endpoint

```bash
curl -X DELETE http://localhost:5000/api/v1/reviews/<review_id>
```

* Expected output:

```json
{
    "message": "Review deleted successfully"
}
```

# Authors

This project was made for `Holberton School Bordeaux` by

[Anthony Goutieras](https://github.com/AGoutieras)

[Anthony Di Domenico](https://github.com/anthodido)
