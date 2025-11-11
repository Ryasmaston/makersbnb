from lib.user import User
from lib.user_repository import UserRepository
from lib.booking import Booking
from datetime import date
from lib.listing import Listing

# Can return all users in the current database
def test_get_all_users(db_connection): # See conftest.py to learn what `db_connection` is.
    db_connection.seed("seeds/makersbnb.sql")
    repository = UserRepository(db_connection)
    users = repository.all()
    assert users == [
        User(1, 'Alice Johnson', 'alice@example.com', 'password123'),
        User(2, 'Bob Smith', 'bob@example.com', 'securepass'),
        User(3, 'Charlie Brown', 'charlie@example.com', 'letmein')
    ]

# Can get a single user by user ID
def test_get_single_user(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = UserRepository(db_connection)
    user = repository.find(1)
    assert user == User(1, 'Alice Johnson', 'alice@example.com', 'password123')


# Can create a new user
def test_create_user(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = UserRepository(db_connection)
    repository.create(User(None, 'Dan Smith', 'dan@example.com', 'coolpassword'))
    result = repository.all()
    assert result == [
        User(1, 'Alice Johnson', 'alice@example.com', 'password123'),
        User(2, 'Bob Smith', 'bob@example.com', 'securepass'),
        User(3, 'Charlie Brown', 'charlie@example.com', 'letmein'),
        User(4, 'Dan Smith', 'dan@example.com', 'coolpassword')
    ]


# Can delete a user
def test_delete_user(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = UserRepository(db_connection)
    repository.delete(1)
    result = repository.all()
    assert result == [
        User(2, 'Bob Smith', 'bob@example.com', 'securepass'),
        User(3, 'Charlie Brown', 'charlie@example.com', 'letmein')
    ]

def test_get_users_bookings(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = UserRepository(db_connection)
    bookings = repository.get_users_bookings(2)
    assert bookings == [
        Booking(1, date(2025, 4, 1), date(2025, 4, 5), 1, 2, 'confirmed'),
        Booking(3, date(2025, 7, 20), date(2025, 7, 25), 3, 2, 'cancelled')
    ]

def test_get_users_listings(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = UserRepository(db_connection)
    listings = repository.get_users_listings(1)
    assert listings == [
        Listing(1, 'Cozy Cabin in the Woods', 'A small rustic cabin with beautiful forest views.', 120, date(2025, 1, 1), date(2025, 12, 31), 1),
        Listing(3, 'Beachside Bungalow', 'Steps away from the ocean with amazing sunsets.', 180, date(2025, 3, 15), date(2025, 11, 15), 1)
    ]
