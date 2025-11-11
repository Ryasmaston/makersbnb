from lib.listing_repository import ListingRepository
from lib.listing import Listing
from datetime import date

"""
When we call ListingRepository.all()
We get a list of Listing objects reflecting the seed data.
"""
def test_get_all_records(db_connection): # See conftest.py to learn what `db_connection` is.
    db_connection.seed('seeds/makersbnb.sql') # Seed our database with some test data
    repository = ListingRepository(db_connection) # Create a new ListingRepository

    listings = repository.all() # Get all listings

    # Assert on the results
    assert listings == [
        Listing(1, 'Cozy Cabin in the Woods', 'A small rustic cabin with beautiful forest views.', 120, date(2025, 1, 1), date(2025, 12, 31), 1),
        Listing(2, 'Modern Apartment Downtown', 'Close to shops, cafes, and nightlife.', 200, date(2025, 2, 1), date(2025, 8, 31), 2),
        Listing(3, 'Beachside Bungalow', 'Steps away from the ocean with amazing sunsets.', 180, date(2025, 3, 15), date(2025, 11, 15), 1)
    ]
"""
When we call ListingRepository.find()
We get a single Listing object reflecting the seed data.
"""
def test_get_single_record(db_connection):
    db_connection.seed('seeds/makersbnb.sql')
    repository = ListingRepository(db_connection)

    listing = repository.find(3)
    assert listing == Listing(3, 'Beachside Bungalow', 'Steps away from the ocean with amazing sunsets.', 180, date(2025, 3, 15), date(2025, 11, 15), 1)

"""
When we call ListingRepository.create()
We get a new record in the database.
"""
def test_create_record(db_connection):
    db_connection.seed('seeds/makersbnb.sql')
    repository = ListingRepository(db_connection)

    repository.create(Listing(4, 'Osmaston Manor', 'Not a shed!', 200, date(1850, 3, 3), date(1965, 4, 21), 3))

    result = repository.all()
    assert result == [
        Listing(1, 'Cozy Cabin in the Woods', 'A small rustic cabin with beautiful forest views.', 120, date(2025, 1, 1), date(2025, 12, 31), 1),
        Listing(2, 'Modern Apartment Downtown', 'Close to shops, cafes, and nightlife.', 200, date(2025, 2, 1), date(2025, 8, 31), 2),
        Listing(3, 'Beachside Bungalow', 'Steps away from the ocean with amazing sunsets.', 180, date(2025, 3, 15), date(2025, 11, 15), 1),
        Listing(4, 'Osmaston Manor', 'Not a shed!', 200, date(1850, 3, 3), date(1965, 4, 21), 3)
    ]

"""
When we call ListingRepository.delete()
We remove a record from the database.
"""
def test_delete_record(db_connection):
    db_connection.seed('seeds/makersbnb.sql')
    repository = ListingRepository(db_connection)
    repository.delete(3) # Bye trump!

    result = repository.all()
    assert result == [
        Listing(1, 'Cozy Cabin in the Woods', 'A small rustic cabin with beautiful forest views.', 120, date(2025, 1, 1), date(2025, 12, 31), 1),
        Listing(2, 'Modern Apartment Downtown', 'Close to shops, cafes, and nightlife.', 200, date(2025, 2, 1), date(2025, 8, 31), 2)
    ]

"""
When we call ListingRepository.get_valid_dates_of_listing(listing_id)
Return the start_available_dates, end_available_dates for listing_id
"""
def test_get_available_dates():
    pass

def test_get_available_listings_between_dates(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = ListingRepository(db_connection)
    start, end = date(2025, 10, 16), date(2025, 11, 8)
    listings = repository.get_available_listings_between_dates(start, end)
    assert listings == [
        Listing(1, "Cozy Cabin in the Woods", "A small rustic cabin with beautiful forest views.", 120, date(2025, 1, 1), date(2025, 12, 31), 1),
        Listing(3, "Beachside Bungalow", "Steps away from the ocean with amazing sunsets.", 180, date(2025, 3, 15), date(2025, 11, 15), 1),
    ]

"""
When we call get_available_listing_for_dates
"""
def test_get_available_listings_between_dates_all_valid(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = ListingRepository(db_connection)
    start, end = date(2025, 3, 16), date(2025, 3, 18)
    listings = repository.get_available_listings_between_dates(start, end)
    assert listings == [
        Listing(1, "Cozy Cabin in the Woods", "A small rustic cabin with beautiful forest views.", 120, date(2025, 1, 1), date(2025, 12, 31), 1),
        Listing(2, "Modern Apartment Downtown", "Close to shops, cafes, and nightlife.", 200, date(2025, 2,  1), date(2025, 8, 31), 2),
        Listing(3, "Beachside Bungalow", "Steps away from the ocean with amazing sunsets.", 180, date(2025, 3, 15), date(2025, 11, 15), 1),
    ]