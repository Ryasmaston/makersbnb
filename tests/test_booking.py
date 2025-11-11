from lib.booking import Booking

def test_booking_constructs():
    booking = Booking(1, '2025-04-01', '2025-04-05', 1, 2, 'confirmed')
    assert booking.end_date == '2025-04-05'
    assert booking.status == "confirmed"
    assert booking.listing_id == 1

"""
We can format artists to strings nicely
"""
def test_bookings_format_nicely():
    booking = Booking(1, '2025-04-01', '2025-04-05', 1, 2, 'confirmed')
    assert str(booking) == "Booking(1, 2025-04-01, 2025-04-05, 1, 2, confirmed)"
    # Try commenting out the `__repr__` method in lib/artist.py
    # And see what happens when you run this test again.

"""
We can compare two identical artists
And have them be equal
"""
def test_artists_are_equal():
    booking1 = Booking(1, '2025-04-01', '2025-04-05', 1, 2, 'confirmed')
    booking2 = Booking(1, '2025-04-01', '2025-04-05', 1, 2, 'confirmed')
    assert booking1 == booking2
    # Try commenting out the `__eq__` method in lib/artist.py
    # And see what happens when you run this test again.