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
