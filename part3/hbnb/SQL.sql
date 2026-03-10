-- entire database schema for the HBnB project
CREATE TABLE User 
(
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE Place
(
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    price DECIMAL(10, 2),
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36),
    FOREIGN KEY (owner_id) REFERENCES User (id)
);


CREATE TABLE Review
(
    id CHAR(36) PRIMARY KEY,
    text TEXT,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    user_id CHAR(36),
    place_id CHAR(36),
    UNIQUE (user_id, place_id),
    FOREIGN KEY (user_id) REFERENCES User (id),
    FOREIGN KEY (place_id) REFERENCES Place (id)
);


CREATE TABLE Amenity
(
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);

CREATE TABLE Place_Amenity
(
    place_id CHAR(36),
    amenity_id CHAR(36),
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES Place (id),
    FOREIGN KEY (amenity_id) REFERENCES Amenity (id)
);

INSERT INTO User (
    id,
    email,
    first_name,
    last_name,
    password,
    is_admin
)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'admin@hbnb.io',
    'Admin',
    'HBnB',
    '$2b$12$9/df6Wj02cKu7.7VJ5nmfeKsvfwswtkZpj.TRTVBfk3K413vjIxs6',
    TRUE
);


INSERT INTO Amenity (id, name)
VALUES
('9dace157-42d8-4424-8167-4773b982bedb', 'Wifi'),
('aa339e07-206d-4969-84bb-c9f691d3b83b', 'Swimming Pool'),
('0b6f16cd-23b7-4d90-8c0d-5e1561847775', 'Air Conditioning');
