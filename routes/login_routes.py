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
        if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
            session.pop('user_id', None)
            email = request.form['email']
            password = request.form['password']

            user = repository.login(email, password)

            if user:
                session['loggedin'] = True
                session['user_id'] = user.id
                session['name'] = user.name
                session['email'] = user.email
                return redirect(url_for('get_listings'))
            else:
                return render_template('index.html', fail=True)

        return render_template('index.html')

    @app.route('/logout')
    def logout():
        session.pop('loggedin', None)
        session.pop('user_id', None)
        session.pop('name', None)
        session.pop('email', None)
        return redirect(url_for('login'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        connection = get_flask_database_connection(app)
        repository = UserRepository(connection)
        if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
            name = request.form['name']
            password = request.form['password']
            email = request.form['email']

            user = User(None, name, email, password)
            repository.create(user)
            user = repository.login(email, password)
            if user:
                session['loggedin'] = True
                session['user_id'] = user.id
                session['name'] = user.name
                session['email'] = user.email
                return redirect(url_for('get_listings'))
            return redirect(url_for('listings'))

        return render_template('register.html')
