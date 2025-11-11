from lib.user import User
from lib.booking import Booking
from lib.listing import Listing

class UserRepository:
    def __init__(self, connection):
        self._connection = connection


    def all(self):
        rows = self._connection.execute('SELECT * FROM users')
        users = []
        for row in rows:
            item = User(row['id'], row['name'], row['email'], row['password'])
            users.append(item)
        return users


    def find(self, user_id):
        rows = self._connection.execute('SELECT * FROM users WHERE id = %s', [user_id])
        row = rows[0]
        return User(row['id'], row['name'], row['email'], row['password'])


    def create(self, user):
        rows = self._connection.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING id', [user.name, user.email, user.password])
        row = rows[0]
        user.id = row['id']
        return user

    def delete(self, user_id):
        self._connection.execute('DELETE FROM users WHERE id = %s', [user_id])
        return None

    def get_users_bookings(self, user_id):
        rows = self._connection.execute(
            'SELECT * FROM bookings WHERE guest_id = %s', [user_id]
        )
        bookings = []
        for row in rows:
            item = Booking(row["id"], row["start_date"],row["end_date"], row["listing_id"], row["guest_id"],row["status"])
            bookings.append(item)
        return bookings

    def get_users_listings(self, user_id):
        rows = self._connection.execute(
            'SELECT * FROM listings WHERE host_id = %s', [user_id]
        )
        listings = []
        for row in rows:
            item = Listing(row["id"], row["title"], row["description"], row["price_per_night"], row["start_available_date"], row["end_available_date"], row["host_id"])
            listings.append(item)
        return listings
    
    def login(self, username, password):
        rows = self._connection.execute(
            'SELECT * FROM users WHERE name = %s AND password = %s', [username, password]
        )
        row = rows[0]
        return  User(row['id'], row['name'], row['email'], row['password'])
