import os
from flask import Flask, request, render_template, session, redirect, url_for
from flask import Flask, request, render_template, session
from flask.helpers import get_flashed_messages
from lib.booking_repository import BookingRepository
from lib.database_connection import get_flask_database_connection
from lib.listing_repository import ListingRepository
from lib.booking import Booking
from datetime import date
from lib.listing import Listing


# Create a new Flask app
app = Flask(__name__)
app.secret_key = 'makersbnb_secret_key'

# == Your Routes Here ==

# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5001/index
@app.route('/', methods=['GET'])
def get_index():
    return render_template('index.html', user=session)

#   ; open http://localhost:5001/index

# @app.route('/sessions/new', methods=['GET'])
# def get_login_page():
#     pass

@app.route('/listings', methods=['GET'])
def get_listings():
    connection = get_flask_database_connection(app)
    listing_repo = ListingRepository(connection)
    booking_repo = BookingRepository(connection)

    # Get filter parameters from query string
    title = request.args.get('title', '').strip()
    description = request.args.get('description', '').strip()
    price_sort = request.args.get('price-filter')
    date_range = request.args.get('filter_date_range', '').strip()

    # Parse date range if provided
    start_date = None
    end_date = None
    if date_range and ' to ' in date_range:
        dates = date_range.split(' to ')
        start_date = dates[0].strip()
        end_date = dates[1].strip()

    # Get filtered listings
    listings = listing_repo.filter(
        title=title if title else None,
        description=description if description else None,
        price_sort=price_sort,
        start_date=start_date,
        end_date=end_date
    )

    # get confirmed dates per listing
    confirmed_dates_by_listing = {}
    for listing in listings:
        confirmed_dates_by_listing[listing.id] = booking_repo.get_confirmed_booking_dates_for_listing(listing.id)

    return render_template('listings.html', user=session, listings=listings, confirmed_dates=confirmed_dates_by_listing)

@app.route('/listings', methods=['POST'])
def post_listings():
    connection = get_flask_database_connection(app)
    listing_repo = ListingRepository(connection)
    print(request.form)
    title = request.form['title']
    description = request.form['description']
    price_per_night = request.form['price_per_night']
    host_id = session['user_id']
    dates = request.form['available_date_range']
    start_date_string = dates[0:10]
    end_date_string = dates[14:24]
    start_year, start_month, start_day = start_date_string.split('-')
    end_year, end_month, end_day = end_date_string.split('-')
    start_available_date = date(int(start_year), int(start_month), int(start_day))
    end_available_date = date(int(end_year), int(end_month), int(end_day))

    new_listing = Listing(None, title, description, price_per_night, start_available_date, end_available_date, host_id)
    listing_repo.create(new_listing)
    return redirect(url_for('get_listings'))

@app.route('/bookings', methods=['GET'])
def get_bookings():
    connection = get_flask_database_connection(app)
    booking_repo = BookingRepository(connection)
    outbound_bookings = booking_repo.all_with_guest_id_join_listings(session['user_id'])
    inbound_bookings = booking_repo.all_with_host_id_join_listings(session['user_id'])
    return render_template('bookings.html', user=session, outbound_bookings=outbound_bookings, inbound_bookings=inbound_bookings)

@app.route('/bookings/new', methods=['POST'])
def post_bookings():
    connection = get_flask_database_connection(app)
    booking_repo = BookingRepository(connection)
    status = 'pending'
    guest_id = session['user_id']
    listing_id = request.form['listing_id']
    dates = request.form['dates_range']
    start_date_string = dates[0:10]
    end_date_string = dates[14:24]
    start_year, start_month, start_day = start_date_string.split('-')
    end_year, end_month, end_day = end_date_string.split('-')
    start_date = date(int(start_year), int(start_month), int(start_day))
    end_date = date(int(end_year), int(end_month), int(end_day))
    new_booking = Booking(None, start_date, end_date, listing_id, guest_id, status)
    booking_repo.create(new_booking)
    return redirect(url_for('get_bookings'))

@app.route('/bookings/<booking_id>/confirm', methods=['POST'])
def confirm_booking(booking_id):
    connection = get_flask_database_connection(app)
    booking_repo = BookingRepository(connection)
    booking_repo.approve_booking(booking_id)
    return redirect(url_for('get_bookings'))

@app.route('/bookings/<booking_id>/reject', methods=['POST'])
def reject_booking(booking_id):
    connection = get_flask_database_connection(app)
    booking_repo = BookingRepository(connection)
    booking_repo.deny_booking(booking_id)
    return redirect(url_for('get_bookings'))

@app.route('/bookings/<booking_id>/cancel', methods=['POST'])
def cancel_booking(booking_id):
    connection = get_flask_database_connection(app)
    booking_repo = BookingRepository(connection)
    booking_repo.cancel_booking(booking_id)
    return redirect(url_for('get_bookings'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error_page.html', user=session, error=error), 404


from routes.login_routes import apply_login_route
apply_login_route(app)
# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
