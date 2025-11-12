import os
from flask import Flask, request, render_template, session
from lib.database_connection import get_flask_database_connection

# Create a new Flask app
app = Flask(__name__)

# == Your Routes Here ==

# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5001/index
@app.route('/index', methods=['GET'])
def get_index():
    message = "Hello, this is passed into the base"
    return render_template('index.html', message=message)


# @app.route('/sessions/new', methods=['GET'])
# def get_login_page():
#     pass

# @app.route('/listings', methods=['GET'])
# def get_login_page():
#     pass

# @app.route('/listings/new', methods=['POST'])
# def get_login_page():
#     pass


# @app.route('/listings/<id>', methods=['GET'])
# def get_login_page():
#     pass

# @app.route('/requests', methods=['GET'])
# def get_login_page():
#     pass

# @app.route('/requests/<id>', methods=['GET'])
# def get_login_page():
#     pass
@app.route('/requests/<id>', methods=['GET'])
def get_login_page():
    pass

from routes.login_routes import apply_login_route
apply_login_route(app)
# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
