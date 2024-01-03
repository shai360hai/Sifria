class Book:
    def __init__(self, name, author, year_published, book_type, idnumber=None):
        self.idnumber = idnumber
        self.name = name
        self.author = author
        self.year_published = year_published
        self.type = book_type
        
        
