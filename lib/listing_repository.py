from lib.listing import Listing

class ListingRepository:

    # We initialise with a database connection
    def __init__(self, connection):
        self._connection = connection

    # Retrieve all listings
    def all(self):
        rows = self._connection.execute('SELECT * from listings')
        listings = []
        for row in rows:
            item = Listing(row["id"], row["title"], row["description"], row["price_per_night"], row["start_available_date"], row["end_available_date"], row["host_id"])
            listings.append(item)
        return listings

    # Find a single listing by their id
    def find(self, list_id):
        rows = self._connection.execute('SELECT * FROM listings WHERE id = %s', [list_id])
        row = rows[0]
        return Listing(row["id"], row["title"], row["description"], row["price_per_night"], row["start_available_date"], row["end_available_date"], row["host_id"])

    # Create a new listing
    # Do you want to get its id back? Look into RETURNING id;
    def create(self, listing):
        self._connection.execute('INSERT INTO listings (title, description, price_per_night, start_available_date, end_available_date, host_id) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id', [listing.title, listing.description, listing.price_per_night, listing.start_available_date, listing.end_available_date, listing.host_id])
        return None

    def update(self, listing):
        self._connection.execute('UPDATE listings SET title = %s, description = %s, price_per_night = %s, start_date = %s, end_date = %s host_id = %s,  WHERE id = %s', [listing.title, listing.description, listing.price, listing.start_available_date, listing.end_available_date, listing.host_id, listing.id])

    # Delete an listing by their id
    def delete(self, listing_id):
        self._connection.execute('DELETE FROM listings WHERE id = %s', [listing_id])
        return None