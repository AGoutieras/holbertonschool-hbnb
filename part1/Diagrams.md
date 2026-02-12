<a href="#"><img src="https://img.shields.io/badge/Mermaid-FF3670?style=for-the-badge&logo=mermaid&logoColor=white"/></a>
[![Holberton](https://img.shields.io/badge/Holberton-E31C3F.svg?style=for-the-badge)](https://www.holbertonschool.fr/)

# HBnB Technical Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [High-Level Architecture](#high-level-architecture)
3. [Business Logic Layer](#business-logic-layer)

---

## Introduction

**Purpose:**
This document compiles all the diagrams and explanatory notes for the HBnB project. It serves as a detailed blueprint guiding the implementation phases and providing a clear reference for the system’s architecture and design.

**Scope:**
- Overview of HBnB project architecture
- Layered design and interaction patterns
- Detailed class definitions and relationships
- API interaction flows with sequence diagrams
- Explanatory notes to clarify design decisions

---

## High-Level Architecture

**Purpose of this Diagram:**
Illustrates the overall structure of HBnB, highlighting the main layers and modules, and showing how they interact.

**Diagram:**
```mermaid
classDiagram
%% --- Presentation Layer ---
class PresentationLayer {
    <<Interface>>
    +ServiceAPI
}

%% --- Business Logic Layer ---
class BusinessLogicLayer {
    +User
    +Place
    +Review
    +Amenity
    +BusinessFacade
}

%% --- Persistence Layer ---
class PersistenceLayer {
    +UserRepo
    +PlaceRepo
    +ReviewRepo
    +AmenityRepo
    +Database
}

%% --- Relations ---
PresentationLayer --> BusinessLogicLayer : Facade Pattern
BusinessLogicLayer --> PersistenceLayer : Database Operations
```

**Explanatory Notes:**
- **Layers Overview:**
  - **Presentation Layer:** Handles user interface and interaction.
  - **Business Logic Layer:** Core functionality and business rules.
  - **Persistence Layer:** Data storage and retrieval.
- **Design Decisions:**
  - Layered architecture allows modular development and separation of concerns.
  - Use of **Facade Pattern** simplifies interactions between layers.
- **Integration:**
  - Each layer communicates through well-defined interfaces, ensuring maintainability and scalability.

---

## Business Logic Layer

**Purpose of this Diagram:**
Provides a detailed view of the Business Logic Layer, showing the main entities, their attributes, and relationships.

**Diagram:**
```mermaid
classDiagram

class User {
    id : UUID
    first_name : String
    last_name : String
    email : String
    password : String
    is_admin : Boolean
    created_at : DateTime
    updated_at : DateTime

    +create()
    +update()
    +delete()
}

class Place {
    id : UUID
    title : String
    description : String
    price : Float
    latitude : Float
    longitude : Float
    created_at : DateTime
    updated_at : DateTime

    +create()
    +update()
    +delete()
}

class Review {
    id : UUID
    rating : Integer
    comment : String
    created_at : DateTime
    updated_at : DateTime

    +create()
    +update()
    +delete()
}

class Amenity {
    id : UUID
    name : String
    description : String
    created_at : DateTime
    updated_at : DateTime

    +create()
    +update()
    +delete()
}

class BusinessFacade {
    +createUser()
    +createPlace()
    +createReview()
    +createAmenity()
}

User "1" --> "*" Place : owns
User "1" --> "*" Review : writes
Place "1" --> "*" Review : receives
Place "*" --> "*" Amenity : has
BusinessFacade --> User
BusinessFacade --> Place
BusinessFacade --> Review
BusinessFacade --> Amenity

```

**Explanatory Notes:**
- **Key Entities:**
  - `User` – Represents registered users of HBnB.
  - `Place` – Represents accommodations available for booking.
  - `Review` – Represents user reviews for places.
  - `Amenity` – Represents facilities available in each place.
  - `BusinessFacade` – Provides simplified access to business logic functions.
- **Relationships:**
  - `User` can write multiple `Reviews`.
  - `Place` contains multiple `Amenities`.
  - `BusinessFacade` coordinates operations across entities.
- **Design Decisions:**
  - Use of `Facade` centralizes logic and reduces direct coupling.
  - Each entity encapsulates its own behavior and data integrity rules.

---

```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

%% 1) User Registration
rect rgba(80,80,255,0.10)
User->>API: Register (POST /users)
API->>BusinessLogic: validate + create user
BusinessLogic->>Database: save user
Database-->>BusinessLogic: ok / error
BusinessLogic-->>API: result
API-->>User: success / failure
end

%% 2) Place Creation
rect rgba(80,255,80,0.10)
User->>API: Create Place (POST /places)
API->>BusinessLogic: validate + create place
BusinessLogic->>Database: save place
Database-->>BusinessLogic: ok / error
BusinessLogic-->>API: result
API-->>User: success / failure
end

%% 3) Review Submission
rect rgba(255,80,80,0.10)
User->>API: Submit Review (POST /places/{id}/reviews)
API->>BusinessLogic: validate + create review
BusinessLogic->>Database: save review
Database-->>BusinessLogic: ok / error
BusinessLogic-->>API: result
API-->>User: success / failure
end

%% 4) Fetch Places List
rect rgba(255,200,80,0.10)
User->>API: List Places (GET /places?filters)
API->>BusinessLogic: validate filters + build query
BusinessLogic->>Database: fetch places
Database-->>BusinessLogic: places[]
BusinessLogic-->>API: places[]
API-->>User: 200 OK (list)
end
```
The 4 actors in the diagram
	•	User: the end user (or a tool like Postman) that triggers an action by sending an HTTP request.
	•	API (Presentation Layer): the entry point of the application. It receives the request, checks that the data is consistent (required fields, formats, query parameters), and prepares the HTTP response.
	•	BusinessLogic (Business Layer): the “business” layer. It applies the application rules (object creation, validations, decisions) and orchestrates the required operations.
	•	Database (Persistence Layer): the persistence layer. It stores information (save) or returns results (fetch) from the database.

⸻

User Registration — Sign up a new user

The user sends a registration request. The API validates the basic information, then forwards it to the business logic which creates the user. The database then stores the new user. Finally, the result is returned: success if the account is created, otherwise failure if something goes wrong.

⸻

Place Creation — Create a listing

The user creates a “place” (a listing). The API checks the submitted data, the business logic builds the place object and applies the necessary rules, then the database saves the listing. The response indicates whether the creation succeeded or not.

⸻

Review Submission — Submit a review

The user submits a review for a place. The API validates the content (for example the text and rating), the business logic creates the review, then the database stores it. As with the other calls, the final response indicates success or error.

⸻

Fetching a List of Places — Retrieve a list

The user requests a list of places based on certain criteria. The API validates and interprets the parameters, the business logic builds the search, then the database returns a list of results. The API then returns a 200 OK response containing the list.

