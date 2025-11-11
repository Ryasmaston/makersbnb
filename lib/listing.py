class Listing:
    def __init__(self, id, title, description, price_per_night, start_available_date, end_available_date, host_id):
        self.id = id
        self.title = title
        self.description = description
        self.price_per_night = price_per_night
        self.start_available_date = start_available_date
        self.end_available_date = end_available_date
        self.host_id = host_id

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"Listing({self.id}, {self.title}, {self.description}, {self.price_per_night}, {self.start_available_date}, {self.end_available_date}, {self.host_id})"