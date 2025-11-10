class Booking : 
    def __init__(self, id, guest_id, listing_id, start_date, end_date, status): 
        self.id = id
        self.guest_id = guest_id
        self.listing_id = listing_id
        self.start_date = start_date
        self.end_date = end_date
        self.status = status

    def __eq__(self, other):
        return self.__dict__ == other.__dict 
    def __repr__(self):
        return f"Booking details:{self.start_date},{self.end_date},{self.listing_id},{self.guest_id},{self.status}"
     
