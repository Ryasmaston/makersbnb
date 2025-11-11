from lib.listing import Listing

"""
Listing constructs with an id, title, release_year, and artist_id
"""
def test_listing_constructs():
    listing = Listing(1, "Tek House", "Crap shed.", 20, "28-07-2025", "14-08-2025", 4)
    assert listing.id == 1
    assert listing.title == "Tek House"
    assert listing.description == "Crap shed."
    assert listing.price_per_night == 20
    assert listing.start_available_date == "28-07-2025"
    assert listing.end_available_date == "14-08-2025"
    assert listing.host_id == 4

"""
We can format listings to strings nicely
"""
def test_listing_format_nicely():
    listing = Listing(1, "Tek House", "Crap shed.", 20, "28-07-2025", "14-08-2025", 4)
    assert str(listing) == "Listing(1, Tek House, Crap shed., 20, 28-07-2025, 14-08-2025, 4)"
    # Try commenting out the `__repr__` method in lib/listing.py
    # And see what happens when you run this test again.

"""
We can compare two identical listings
And have them be equal
"""
def test_listings_are_equal():
    listing1 = Listing(1, 4, "Tek House", "Crap shed.", 20, "28-07-2025", "14-08-2025")
    listing2 = Listing(1, 4, "Tek House", "Crap shed.", 20, "28-07-2025", "14-08-2025")
    assert listing1 == listing2
    # Try commenting out the `__eq__` method in lib/listing .py
    # And see what happens when you run this test again.