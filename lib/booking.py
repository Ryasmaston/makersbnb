class Booking : 
    def __init__(self, id, start_date, end_date, listing_id, guest_id, status): 
        self.id = id
        self.guest_id = guest_id
        self.listing_id = listing_id
        self.start_date = start_date
        self.end_date = end_date
        self.status = status

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    def __repr__(self):
        return f"Booking({self.id}, {self.start_date}, {self.end_date}, {self.listing_id}, {self.guest_id}, {self.status})"
