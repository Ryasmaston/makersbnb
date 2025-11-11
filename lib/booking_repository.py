from lib.booking import Booking
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

    def approve_booking(self, booking_id):
        """
        Set booking from 'pending' -> 'confirmed'.
        Returns True if updated, False otherwise.
        """
        sql = """
        UPDATE bookings
        SET status = 'confirmed'
        WHERE id = %s AND status = 'pending'
        RETURNING id;
        """
        rows = self._connection.execute(sql, [booking_id])
        return bool(rows)



