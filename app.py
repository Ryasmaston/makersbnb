import os
<<<<<<< HEAD
from flask import Flask, request, render_template, session, redirect, url_for
=======
from flask import Flask, request, render_template, session
from flask.helpers import get_flashed_messages
from lib.booking_repository import BookingRepository
>>>>>>> 1f5d8579e864f8907657c20b66a1b1eaee9df8d9
from lib.database_connection import get_flask_database_connection
from lib.listing_repository import ListingRepository
from lib.booking_repository import BookingRepository
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
    listings = listing_repo.all()

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
    booking_repo = BookingRepository(get_flask_database_connection(app))
    outbound_bookings = booking_repo.all_with_guest_id(session['user_id'])
    inbound_bookings = booking_repo.all_with_host_id(session['user_id'])
    return render_template('bookings.html', outbound_bookings=outbound_bookings, inbound_bookings=inbound_bookings)

# @app.route('/listings/new', methods=['POST'])
# def get_login_page():
#     pass


# @app.route('/listings/<id>', methods=['GET'])
# def get_login_page():
#     pass

# @app.route('/requests', methods=['GET'])
# def get_login_page():
#     pass

# @app.route('/requests/<id>', methods=['GET'])
# def get_login_page():
#     pass


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
