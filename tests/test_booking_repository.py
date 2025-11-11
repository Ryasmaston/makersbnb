from lib.booking_repository import BookingRepository
from lib.booking import Booking
from datetime import date

def test_all_bookings(db_connection):
    db_connection.seed("./seeds/makersbnb.sql")
    repo = BookingRepository(db_connection)
    bookings = repo.all()

    assert bookings == [
        Booking(1, date(2025, 4, 1), date(2025, 4, 5), 1, 2, 'confirmed'),
        Booking(2, date(2025, 5, 10), date(2025, 5, 15), 2, 3, 'pending'),
        Booking(3, date(2025, 7, 20), date(2025, 7, 25), 3, 2, 'cancelled')
    ]

def test_get_single_booking(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repo = BookingRepository(db_connection)
    booking = repo.find(1)


    assert booking == Booking(1, date(2025, 4, 1), date(2025, 4, 5), 1, 2, 'confirmed')

def test_create_booking(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repo = BookingRepository(db_connection)


    repo.create(Booking(None, date(2025, 6, 28), date(2025, 6, 30), 1, 2, 'pending'))
    bookings = repo.all()

    assert bookings == [
        Booking(1, date(2025, 4, 1), date(2025, 4, 5), 1, 2, 'confirmed'),
        Booking(2, date(2025, 5, 10), date(2025, 5, 15), 2, 3, 'pending'),
        Booking(3, date(2025, 7, 20), date(2025, 7, 25), 3, 2, 'cancelled'),
        Booking(4, date(2025, 6, 28), date(2025, 6, 30), 1, 2, 'pending')
    ]

def test_delete_booking(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repo = BookingRepository(db_connection)
    repo.delete(1)
    bookings = repo.all()


    assert bookings == [
        Booking(2, date(2025, 5, 10), date(2025, 5, 15), 2, 3, 'pending'),
        Booking(3, date(2025, 7, 20), date(2025, 7, 25), 3, 2, 'cancelled')
    ]


def test_total_price(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repo = BookingRepository(db_connection)
    assert repo.total_price(1) == 4 * 120

def test_approve_booking(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repo = BookingRepository(db_connection)

    updated = repo.approve_booking(2)
    assert updated is True

    b2 = repo.find(2)
    assert b2.status == "confirmed"

    updated_again = repo.approve_booking (2)
    assert updated_again is False
