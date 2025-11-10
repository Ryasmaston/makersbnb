from lib.booking import Booking
class BookingRepository:
    def __init__(self, connection):
        self.connection = connection 
    def all(self):
        array = self.connection.execute('SELECT * FROM bookings')
        bookings = []
        for item in array:
            booking = Booking(item["start_date"],item["end_date"], item["listing_id"], item["guest_id"],item["status"])
            bookings.append(booking)
        return bookings
