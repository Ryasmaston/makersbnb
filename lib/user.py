class User:
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password


    def __eq__(self, o):
        return self.__dict__ == o.__dict__
    

    def __repr__(self):
        return f'User({self.id}, {self.name}, {self.email}, {self.password})'

