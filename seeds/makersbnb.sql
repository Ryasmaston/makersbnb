
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS listings;
DROP TABLE IF EXISTS users;


CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE listings (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price_per_night INTEGER NOT NULL,
    start_available_date DATE NOT NULL,
    end_available_date DATE NOT NULL,
    host_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    listing_id INTEGER NOT NULL REFERENCES listings(id) ON DELETE CASCADE,
    guest_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status TEXT DEFAULT 'pending'
);


-- Users
INSERT INTO users (name, email, password) VALUES
('Alice Johnson', 'alice@example.com', 'password123'),
('Bob Smith', 'bob@example.com', 'securepass'),
('Charlie Brown', 'charlie@example.com', 'letmein');

-- Listings
INSERT INTO listings (title, description, price_per_night, start_available_date, end_available_date, host_id) VALUES
('Cozy Cabin in the Woods', 'A small rustic cabin with beautiful forest views.', 120, '2025-01-01', '2025-12-31', 1),
('Modern Apartment Downtown', 'Close to shops, cafes, and nightlife.', 200, '2025-02-01', '2025-08-31', 2),
('Beachside Bungalow', 'Steps away from the ocean with amazing sunsets.', 180, '2025-03-15', '2025-11-15', 1);

-- Bookings
INSERT INTO bookings (start_date, end_date, listing_id, guest_id, status) VALUES
('2025-04-01', '2025-04-05', 1, 2, 'confirmed'),
('2025-05-10', '2025-05-15', 2, 3, 'pending'),
('2025-07-20', '2025-07-25', 3, 2, 'cancelled');


