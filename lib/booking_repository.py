from lib.booking import Booking
from datetime import date
class BookingRepository:
    def __init__(self, connection):
        self._connection = connection
    def all(self):
        array = self._connection.execute('SELECT * FROM bookings')
        bookings = []
        for item in array:
            booking = Booking(item["id"], item["start_date"],item["end_date"], item["listing_id"], item["guest_id"],item["status"])
            bookings.append(booking)
        return bookings

    def find(self, booking_id):
        rows = self._connection.execute(
            'SELECT * FROM bookings WHERE id = %s', [booking_id]
        )

        row = rows[0]
        return Booking(row["id"], row["start_date"],row["end_date"], row["listing_id"], row["guest_id"],row["status"])

    def create(self, booking):
        rows = self._connection.execute(
            'INSERT INTO bookings (start_date, end_date, listing_id, guest_id, status) VALUES (%s, %s, %s, %s, %s) RETURNING id',
            [booking.start_date, booking.end_date, booking.listing_id, booking.guest_id, booking.status]
        )
        row = rows[0]
        booking.id = row["id"]
        return booking

    def delete(self, booking_id):
        self._connection.execute('DELETE FROM bookings WHERE id = %s', [booking_id])
        return None

    def total_price(self, booking_id):
        """
        total = (end_date - start_date in days) * listing.price_per_night
        """
        sql = """
        SELECT
        (b.end_date - b.start_date) * l.price_per_night AS total_price
        FROM bookings b
        JOIN listings l ON l.id = b.listing_id
        WHERE b.id = %s;
        """
        rows = self._connection.execute(sql, [booking_id])
        if not rows or rows[0]["total_price"] is None:
            raise ValueError("Booking not found or dates missing")
        return int(rows[0]["total_price"])

    def get_future_bookings_for_listing(self, listing_id):
            rows = self._connection.execute(
                "SELECT * FROM bookings WHERE listing_id = %s AND start_date >= %s AND status = 'confirmed'",
                [listing_id, date.today()]
            )
            return rows


    def deny_overlapping_bookings(self, booking_id):
        """
        Deny all pending bookings that overlap with the given booking.
        Returns the number of bookings denied.
        """
        # get the booking details
        booking = self.find(booking_id)

        # find all pending bookings for the same listing that overlap
        sql = """
        UPDATE bookings
        SET status = 'denied'
        WHERE listing_id = %s
        AND id != %s
        AND status = 'pending'
        AND start_date < %s
        AND end_date > %s
        RETURNING id;
        """
        rows = self._connection.execute(
            sql,
            [booking.listing_id, booking_id, booking.end_date, booking.start_date]
        )
        return len(rows) if rows else 0

    def approve_booking(self, booking_id):
        """
        Set booking from 'pending' -> 'confirmed'.
        Also denies any overlapping pending bookings for the same listing.
        Returns True if updated, False otherwise.
        """
        sql = """
        UPDATE bookings
        SET status = 'confirmed'
        WHERE id = %s AND status = 'pending'
        RETURNING id;
        """
        rows = self._connection.execute(sql, [booking_id])

        if rows:
            # deny any overlapping pending bookings
            self.deny_overlapping_bookings(booking_id)
            return True

        return False

    def get_confirmed_booking_dates_for_listing(self, listing_id):
        """
        Returns all confirmed booking date ranges for a specific listing.
        Returns a list of dicts with start_date and end_date keys.
        """
        sql = """
        SELECT start_date, end_date
        FROM bookings
        WHERE listing_id = %s AND status = 'confirmed'
        ORDER BY start_date;
        """
        rows = self._connection.execute(sql, [listing_id])
        return [{"start_date": str(row["start_date"]), "end_date": str(row["end_date"])} for row in rows]

    def deny_booking(self, booking_id):
        """
        Set booking from 'pending' -> 'denied'.
        Returns True if updated, False otherwise.
        """
        sql = """
        UPDATE bookings
        SET status = 'denied'
        WHERE id = %s AND status = 'pending'
        RETURNING id;
        """
        rows = self._connection.execute(sql, [booking_id])
        return bool(rows)

    def cancel_booking(self, booking_id):
        """
        Set booking from 'pending' -> 'cancelled'.
        Returns True if updated, False otherwise.
        """
        sql = """
        UPDATE bookings
        SET status = 'cancelled'
        WHERE id = %s AND status = 'pending'
        RETURNING id;
        """
        rows = self._connection.execute(sql, [booking_id])
        return bool(rows)

    def all_with_guest_id(self, guest_id):
        sql = """
        SELECT * FROM bookings WHERE guest_id = %s
        """
        rows = self._connection.execute(sql, [guest_id])
        bookings = [Booking(row['id'], row['start_date'], row['end_date'], row['listing_id'], row['guest_id'], row['status']) for row in rows]
        return bookings

    def all_with_host_id(self, host_id):
        sql = """
        SELECT * FROM bookings JOIN listings ON listings.id = bookings.listing_id WHERE listings.host_id = %s
        """
        rows = self._connection.execute(sql, [host_id])
        bookings = [Booking(row['id'], row['start_date'], row['end_date'], row['listing_id'], row['guest_id'], row['status']) for row in rows]
        return bookings

    def all_with_guest_id_join_listings(self, guest_id):
        sql = """
        SELECT
            bookings.id,
            bookings.start_date,
            bookings.end_date,
            bookings.listing_id,
            bookings.guest_id,
            bookings.status,
            listings.title as listing_title,
            listings.description as listing_description,
            listings.price_per_night as listing_price_per_night,
            listings.host_id as listing_host_id,
            (bookings.end_date - bookings.start_date) * listings.price_per_night as total_price
        FROM bookings
        JOIN listings ON listings.id = bookings.listing_id
        WHERE bookings.guest_id = %s
        ORDER BY bookings.start_date ASC
        """
        rows = self._connection.execute(sql, [guest_id])
        # Return dictionaries with both booking and listing data
        bookings = []
        for row in rows:
            booking_dict = {
                'id': row['id'],
                'start_date': row['start_date'],
                'end_date': row['end_date'],
                'listing_id': row['listing_id'],
                'guest_id': row['guest_id'],
                'status': row['status'],
                'listing_title': row['listing_title'],
                'listing_description': row['listing_description'],
                'listing_price_per_night': row['listing_price_per_night'],
                'listing_host_id': row['listing_host_id'],
                'total_price': row['total_price']
            }
            bookings.append(booking_dict)
        return bookings

    def all_with_host_id_join_listings(self, host_id):
        sql = """
        SELECT
            bookings.id,
            bookings.start_date,
            bookings.end_date,
            bookings.listing_id,
            bookings.guest_id,
            bookings.status,
            listings.title as listing_title,
            listings.description as listing_description,
            listings.price_per_night as listing_price_per_night,
            listings.host_id as listing_host_id,
            (bookings.end_date - bookings.start_date) * listings.price_per_night as total_price
        FROM bookings
        JOIN listings ON listings.id = bookings.listing_id
        WHERE listings.host_id = %s
        ORDER BY
            CASE
                WHEN bookings.status = 'pending' THEN 1
                WHEN bookings.status = 'confirmed' THEN 2
                ELSE 3
            END,
            bookings.start_date ASC
        """
        rows = self._connection.execute(sql, [host_id])
        # Return dictionaries with both booking and listing data
        bookings = []
        for row in rows:
            booking_dict = {
                'id': row['id'],
                'start_date': row['start_date'],
                'end_date': row['end_date'],
                'listing_id': row['listing_id'],
                'guest_id': row['guest_id'],
                'status': row['status'],
                'listing_title': row['listing_title'],
                'listing_description': row['listing_description'],
                'listing_price_per_night': row['listing_price_per_night'],
                'listing_host_id': row['listing_host_id'],
                'total_price': row['total_price']
            }
            bookings.append(booking_dict)
        return bookings
