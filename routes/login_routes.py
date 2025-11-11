from lib.database_connection import get_flask_database_connection
from flask import Flask, render_template, request, redirect, url_for, session
from lib.user import User
from lib.user_repository import UserRepository
import re

def apply_login_route(app):
    
    @app.route('/', methods=['GET', 'POST'])
    def login():
        connection = get_flask_database_connection(app)
        repository = UserRepository(connection)
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
        return render_template('index.html')


    @app.route('/sessions/new', methods=['GET', 'POST'])
    def register():
        connection = get_flask_database_connection(app)
        repository = UserRepository(connection)
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']

        
        user = User(None, username, email, password)
        repository.create(user)
        return redirect("login")

