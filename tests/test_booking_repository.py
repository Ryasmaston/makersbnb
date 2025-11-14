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

def test_get_confirmed_booking_dates_for_listing(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repo = BookingRepository(db_connection)

    confirmed_dates = repo.get_confirmed_booking_dates_for_listing(1)

    assert confirmed_dates == [
        {"start_date": "2025-04-01", "end_date": "2025-04-05"}
    ]

def test_all_with_guest_id_join_listings(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repo = BookingRepository(db_connection)

    bookings = repo.all_with_guest_id_join_listings(2)

    assert len(bookings) == 2
    assert bookings[0]['id'] == 1
    assert bookings[0]['listing_title'] == 'Cozy Cabin in the Woods'
    assert bookings[0]['listing_description'] == 'A small rustic cabin with beautiful forest views.'
    assert bookings[0]['total_price'] == 480

def test_all_with_host_id_join_listings(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repo = BookingRepository(db_connection)

    bookings = repo.all_with_host_id_join_listings(1)

    assert len(bookings) == 2
    assert bookings[0]['id'] == 1
    assert bookings[0]['listing_title'] == 'Cozy Cabin in the Woods'
    assert bookings[0]['status'] == 'confirmed'
    assert bookings[0]['total_price'] == 480

def test_cancel_overlapping_bookings(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repo = BookingRepository(db_connection)

    # Create a new pending booking for listing 1
    repo.create(Booking(None, date(2025, 6, 1), date(2025, 6, 5), 1, 3, 'pending'))

    # Create overlapping pending bookings for listing 1
    repo.create(Booking(None, date(2025, 6, 3), date(2025, 6, 7), 1, 3, 'pending'))
    repo.create(Booking(None, date(2025, 6, 6), date(2025, 6, 10), 1, 3, 'pending'))

    # Confirm booking 4 (2025-06-01 to 2025-06-05)
    repo.approve_booking(4)

    # Check that booking 5 was denied (overlaps: 06-03 to 06-07)
    booking_5 = repo.find(5)
    assert booking_5.status == 'denied'

    # Check that booking 6 was NOT denied (doesn't overlap: 06-06 to 06-10)
    booking_6 = repo.find(6)
    assert booking_6.status == 'pending'

def test_all_overlap_scenarios(db_connection):
    """Test all possible overlap scenarios when confirming a booking"""
    db_connection.seed("seeds/makersbnb.sql")
    repo = BookingRepository(db_connection)

    # create the booking we'll confirm: June 10-15 for listing 1
    confirmed_booking = repo.create(Booking(None, date(2025, 6, 10), date(2025, 6, 15), 1, 3, 'pending'))

    # scenario 1: pending booking completely contains confirmed (June 8-20)
    repo.create(Booking(None, date(2025, 6, 8), date(2025, 6, 20), 1, 3, 'pending'))

    # scenario 2: confirmed completely contains pending (June 11-14)
    repo.create(Booking(None, date(2025, 6, 11), date(2025, 6, 14), 1, 3, 'pending'))

    # scenario 3: pending starts before, ends during confirmed (June 8-12)
    repo.create(Booking(None, date(2025, 6, 8), date(2025, 6, 12), 1, 3, 'pending'))

    # scenario 4: pending starts during, ends after confirmed (June 13-18)
    repo.create(Booking(None, date(2025, 6, 13), date(2025, 6, 18), 1, 3, 'pending'))

    # scenario 5: exact match (June 10-15)
    repo.create(Booking(None, date(2025, 6, 10), date(2025, 6, 15), 1, 3, 'pending'))

    # scenario 6: no overlap - before (June 5-8)
    repo.create(Booking(None, date(2025, 6, 5), date(2025, 6, 8), 1, 3, 'pending'))

    # scenario 7: no overlap - after (June 18-22)
    repo.create(Booking(None, date(2025, 6, 18), date(2025, 6, 22), 1, 3, 'pending'))

    # scenario 8: adjacent - ends when confirmed starts (June 8-10)
    repo.create(Booking(None, date(2025, 6, 8), date(2025, 6, 10), 1, 3, 'pending'))

    # scenario 9: adjacent - starts when confirmed ends (June 15-18)
    repo.create(Booking(None, date(2025, 6, 15), date(2025, 6, 18), 1, 3, 'pending'))

    # confirm the booking
    repo.approve_booking(confirmed_booking.id)

    # assert overlapping bookings were denied
    assert repo.find(5).status == 'denied'  # scenario 1: contains confirmed
    assert repo.find(6).status == 'denied'  # scenario 2: contained by confirmed
    assert repo.find(7).status == 'denied'  # scenario 3: starts before, ends during
    assert repo.find(8).status == 'denied'  # scenario 4: starts during, ends after
    assert repo.find(9).status == 'denied'  # scenario 5: exact match

    # assert non-overlapping bookings are pending
    assert repo.find(10).status == 'pending'  # scenario 6: before
    assert repo.find(11).status == 'pending'  # scenario 7: after
    assert repo.find(12).status == 'pending'  # scenario 8: adjacent before
    assert repo.find(13).status == 'pending'  # scenario 9: adjacent after
