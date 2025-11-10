from lib.user import User
from lib.user_repository import UserRepository

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