from bookish.app import db


class BookModel(db.Model):
    # This sets the name of the table in the database
    __tablename__ = 'BookModel'

    # Here we outline what columns we want in our database
    ISBN = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    author = db.Column(db.String())

    def __init__(self, ISBN, title, author):
        self.ISBN = ISBN
        self.title = title
        self.author = author

    def __repr__(self):
        return '<id {}>'.format(self.ISBN)

    def serialize(self):
        return {
            'ISBN': self.ISBN,
            'title': self.title,
            'author': self.author
        }

class BookCopies(db.Model):
    # This sets the name of the table in the database
    __tablename__ = 'BookCopies'

    # Here we outline what columns we want in our database
    BookID = db.Column(db.Integer, primary_key=True)
    ISBN = db.Column(db.Integer)

    def __init__(self, ISBN):
        self.ISBN = ISBN

    def __repr__(self):
        return '<id {}>'.format(self.BookID)

    def serialize(self):
        return {
            'BookID': self.BookID,
            'ISBN': self.ISBN
        }

class BorrowedBooks(db.Model):
    # This sets the name of the table in the database
    __tablename__ = 'BorrowedBooks'

    # Here we outline what columns we want in our database
    BookID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer)
    DueDate = db.Column(db.Date)

    def __init__(self, BookID, UserID, DueDate):
        self.BookID = BookID
        self.UserID = UserID
        self.DueDate = DueDate

    def __repr__(self):
        return '<id {}>'.format(self.BookID)

    def serialize(self):
        return {
            'BookID': self.BookID,
            'UserID': self.UserID,
            'DueDate': self.DueDate
        }

class Users(db.Model):
    # This sets the name of the table in the database
    __tablename__ = 'Users'

    # Here we outline what columns we want in our database
    UserID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<id {}>'.format(self.UserID)

    def serialize(self):
        return {
            'UserID': self.UserID,
            'username': self.username,
            'password': self.password
        }