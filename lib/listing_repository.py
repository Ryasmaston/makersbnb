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
        self._connection.execute('UPDATE listings SET title = %s, description = %s, price_per_night = %s, start_date = %s, end_date = %s, host_id = %s,  WHERE id = %s', [listing.title, listing.description, listing.price_per_night, listing.start_available_date, listing.end_available_date, listing.host_id, listing.id])

    # Delete an listing by their id
    def delete(self, listing_id):
        self._connection.execute('DELETE FROM listings WHERE id = %s', [listing_id])
        return None

    # Gets the start_available_date and end_available_date for a listing.
    def get_available_dates(self, listing_id):
        dates = self._connection.execute('SELECT start_available_date, end_available_date from listings WHERE id = %s', [listing_id])
        return dates

    def get_by_id(self, listing_id):
            rows = self._connection.execute('SELECT * FROM listings WHERE id = %s', [listing_id])
            row = None
            for r in rows:
                row = r
                break
            if row:
                return Listing(
                    row["id"],
                    row["title"],
                    row["description"],
                    row["price_per_night"],
                    row["start_available_date"],
                    row["end_available_date"],
                    row["host_id"]
                )
            return None

    # Returns listings that are available between start_date + end_date
    # And does not clash with any existing, confirmed bookings
    def get_available_listings_between_dates(self, start_date, end_date):
        rows = self._connection.execute("""SELECT * FROM listings
                                        WHERE start_available_date <= %s
                                        AND end_available_date  >= %s
                                        AND id NOT IN (
                                            SELECT listing_id FROM bookings
                                            WHERE status = 'confirmed'
                                            AND NOT (%s > end_date OR %s < start_date)
        )""", [start_date, end_date, start_date, end_date])
        listings = []
        for row in rows:
            item = Listing(row["id"], row["title"], row["description"], row["price_per_night"], row["start_available_date"], row["end_available_date"], row["host_id"])
            listings.append(item)
        return listings

    # Filter and sort listings based on provided criteria
    # Returns all listings if no filters are provided
    def filter(self, title=None, description=None, price_sort=None, start_date=None, end_date=None):
        # Start with base query
        query = "SELECT * FROM listings WHERE 1=1"
        params = []

        # Add title filter if provided
        if title:
            query += " AND title ILIKE %s"
            params.append(f"%{title}%")

        # Add description filter if provided
        if description:
            query += " AND description ILIKE %s"
            params.append(f"%{description}%")

        # Add date range filter if provided
        if start_date and end_date:
            query += " AND start_available_date <= %s AND end_available_date >= %s"
            params.append(start_date)
            params.append(end_date)

        # Add price sorting if provided
        if price_sort == 'ascending':
            query += " ORDER BY price_per_night ASC"
        elif price_sort == 'descending':
            query += " ORDER BY price_per_night DESC"
        else:
            query += " ORDER BY id DESC"  # Default sort by newest

        # Execute query
        rows = self._connection.execute(query, params)

        # Convert rows to Listing objects
        listings = []
        for row in rows:
            item = Listing(
                row["id"],
                row["title"],
                row["description"],
                row["price_per_night"],
                row["start_available_date"],
                row["end_available_date"],
                row["host_id"]
            )
            listings.append(item)

        return listings
