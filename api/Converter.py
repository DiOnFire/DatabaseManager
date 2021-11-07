class Converter:
    def __init__(self, database):
        self.database = database
        self.type = self.get_type()

    def get_type(self):
        return self.database.split(".")[1]

