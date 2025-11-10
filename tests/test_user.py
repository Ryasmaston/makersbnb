from lib.user import User

# Constructs with id, name, email and password
def test_constructs_with_correct_values():
    user = User(1, 'John Doe', 'john@email.com', 'mypassword')
    assert user.id == 1
    assert user.name == 'John Doe'
    assert user.email == 'john@email.com'
    assert user.password == 'mypassword'

# Where two users are constructed with the same values,
# they are equal
def test_equality():
    user1 = User(1, 'John Doe', 'john@email.com', 'mypassword')
    user2 = User(1, 'John Doe', 'john@email.com', 'mypassword')
    assert user1 == user2

# Users are output in a nice format
def test_formatting():
    user = User(1, 'John Doe', 'john@email.com', 'mypassword')
    assert str(user) == 'User(1, John Doe, john@email.com, mypassword)'