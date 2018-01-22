class Book:

    """ Represents one book in a user's list of books"""

    NO_ID = -1

    def __init__(self, title, author, read=False, id=NO_ID, stars=-1, stars_str="", date=""):
        """ Default book is unread, and has no ID """
        self.title = title
        self.author = author
        self.read = read
        self.id = id
        self.date = date
        self.stars = stars
        self.stars_str = stars_str

    def set_id(self, id):
        self.id = id

    def __str__(self):
        read_str = 'no'
        if self.read:
            read_str = 'yes'

        id_str = self.id
        if id == -1:
            id_str = '(no id)'

        template = 'id: {} Title: {} Author: {} Read: {}'
        if self.stars >= 0:
            template += " Stars: {}".format(self.stars_str)
        if self.date != "":
            template += " Date Read: {}".format(self.date)
        return template.format(id_str, self.title, self.author, read_str)

    def __eq__(self, other):
        return self.title == other.title and self.author == other.author and self.read == other.read and self.id == other.id

    def getJSON(self):
        """Iterates over all properties in book object and builds a JSON string"""
        json_str = "{ "
        for attr, value in self.__dict__.items():
            if isinstance(value, bool):
                json_str += "\"{}\": {}, ".format(attr, str(value).lower())
            elif isinstance(value, int):
                json_str += "\"{}\": \"{}\", ".format(attr, value)
            elif attr == "date":
                if value:
                    json_str += "\"{}\": \"{}\", ".format(attr, value)
            elif attr == "stars_str":
                if value:
                    json_str += "\"{}\": \"{}\", ".format(attr, value)
            else:
                json_str += "\"{}\": \"{}\", ".format(attr, value)
        json_str = json_str[:-2]
        json_str += " }"
        return json_str
