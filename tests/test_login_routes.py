import unittest.mock as mock
from flask import Flask
from lib.user import User  # Assumed to be in lib/user.py
# Import the function we want to test
from routes.login_routes import apply_login_route

def test_register_post_creates_user_and_redirects():
    """
    Test that a POST request to /sessions/new with valid data
    creates a new user and redirects to the login page.
    """
    # 1. Set up a minimal Flask app
    app = Flask(__name__)
    # Apply the route from your file
    apply_login_route(app)
    # Get a test client to make requests
    client = app.test_client()

    # 2. Mock dependencies
    # We patch the functions/classes *where they are looked up*
    # (i.e., inside the 'lib.login_route' file)
    
    with mock.patch('routes.login_route.get_flask_database_connection') as mock_get_conn, \
        mock.patch('routes.login_route.UserRepository') as mock_UserRepo:

        # Configure the mocks to return other mocks
        mock_conn = mock.Mock()
        mock_get_conn.return_value = mock_conn
        
        mock_repo_instance = mock.Mock()
        mock_UserRepo.return_value = mock_repo_instance

        # 3. Define the form data we'll send
        form_data = {
            'username': 'test_user',
            'password': 'password123',
            'email': 'test@example.com'
        }

        # 4. Make the simulated POST request
        response = client.post('/sessions/new', data=form_data)

        # 5. Assertions: Check if everything happened as expected

        # Check if we tried to get a connection
        mock_get_conn.assert_called_once_with(app)
        
        # Check if the repository was initialized with that connection
        mock_UserRepo.assert_called_once_with(mock_conn)
        
        # Check that repo.create() was called
        assert mock_repo_instance.create.call_count == 1
        
        # Get the argument that repo.create() was called with
        called_with_user = mock_repo_instance.create.call_args[0][0]
        
        # Check that it's a User object with the correct data
        assert isinstance(called_with_user, User)
        assert called_with_user.id is None
        assert called_with_user.username == 'test_user'
        assert called_with_user.email == 'test@example.com'
        assert called_with_user.password == 'password123'

        # Check that the response was a redirect (HTTP 302)
        assert response.status_code == 302
        
        # Check that it redirected to '/login'
        # redirect("login") resolves to '/login' in the test client
        assert response.location == '/login'