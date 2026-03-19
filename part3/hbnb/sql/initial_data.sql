INSERT INTO users (
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
    '$2b$12$/ZguCnYGNWJz9cbvKi3q4exR2Ed9sTJHbYZqo/rAAyZZBf.Inui82',
    TRUE
);

INSERT INTO amenities (id, name)
VALUES ('0c4804c7-b225-4e0d-9993-4b9a5915fb93', 'WiFi');

INSERT INTO amenities (id, name)
VALUES ('46acbf8f-4a41-4264-8e40-3e774f860fba', 'Swimming Pool');

INSERT INTO amenities (id, name)
VALUES ('e7745087-ed24-4962-a558-4689744f5ce3', 'Air Conditioning');