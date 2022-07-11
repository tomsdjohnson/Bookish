from flask import request
from bookish.models.example import BookModel, BookCopies, BorrowedBooks, Users
from bookish.models import db


def bookish_routes(app):
    @app.route('/healthcheck')
    def health_check():
        return {"status": "OK"}

    @app.route('/AddBook', methods=['POST'])
    def handle_AddBook():
        if request.is_json:

            data = request.get_json()
            new_book_model = BookModel(ISBN=data['ISBN'], title=data['title'], author=data['author'])

            print(BookCopies.query.all())

            for x in range(data['copies']):
                new_book_copy = BookCopies(ISBN=data['ISBN'])
                db.session.add(new_book_copy)

            print(BookCopies.query.all())

            db.session.add(new_book_model)

            db.session.commit()
            return {"message": "New example has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    @app.route('/GetBooks', methods=['GET'])
    def handle_GetBooks():
        books = BookModel.query.order_by(BookModel.title).all()
        results = [
            {
                'ISBN': book.ISBN,
                'title': book.title,
                'author': book.author
            } for book in books]
        return {"Books": results}

    @app.route('/NewUser', methods=['POST'])
    def handle_NewUser():
        data = request.get_json()
        inputUsername = data['username']

        if inputUsername in [user.username for user in Users.query.all()]:
            return {"message" : "Username already taken"}
        else:
            new_user = Users(username=inputUsername, password=data['password'])
            db.session.add(new_user)
            db.session.commit()

            return {"message": "New user has been created successfully."}

    @app.route('/SearchBookByTitle', methods=['GET'])
    def handle_SearchBookByTitle():
        if request.is_json:

            data = request.get_json()
            inputTitle = data['title']

            books = BookModel.query.where(BookModel.title == inputTitle).all()
            if not books:
                return {"error": "No books with that title"}
            results = [
                {
                    'ISBN': book.ISBN,
                    'title': book.title,
                    'author': book.author
                } for book in books]
            return {"Books": results}

        else:
            return {"error": "Wasn't a JSON"}

    @app.route('/SearchBookByAuthor', methods=['GET'])
    def handle_SearchBookByAuthor():
        if request.is_json:

            data = request.get_json()
            inputAuthor = data['author']

            books = BookModel.query.where(BookModel.author == inputAuthor).all()
            if not books:
                return {"error": "No books by that author"}
            results = [
                {
                    'ISBN': book.ISBN,
                    'title': book.title,
                    'author': book.author
                } for book in books]
            return {"Books": results}

        else:
            return {"error": "Wasn't a JSON"}

    @app.route('/BorrowBook', methods=['POST'])
    def handle_BorrowBook():
        if request.is_json:

            data = request.get_json()
            #(ISBN=data['ISBN'], username=data['username'], DueDate=data['DueDate'])
            ISBN = data['ISBN']
            username = data['username']
            DueDate = data['DueDate']

            user = Users.query.where(Users.username == username).all()
            if not user:
                return {"error": "No user by that username"}

            UserID = user[0].UserID

            books = BookCopies.query.where(BookCopies.ISBN == ISBN).all()

            if not books:
                return {"error": "Library does not have this book."}

            book_ids = [book.BookID for book in books]

            for book_id in book_ids:
                book = BorrowedBooks.query.where(BorrowedBooks.BookID == book_id).where(BorrowedBooks.UserID == UserID).all()
                if book:
                    return {"error": "User has already borrowed this book."}


            for book_id in book_ids:
                book = BorrowedBooks.query.where(BorrowedBooks.BookID == book_id).all()
                if not book:
                    new_borrowed_book = BorrowedBooks(BookID=book_id, UserID=UserID, DueDate = DueDate)
                    db.session.add(new_borrowed_book)
                    db.session.commit()
                    return {"message": "Book successfully borrowed."}

            return {"error": "All books are borrowed."}

    @app.route('/ReturnBook', methods=['POST'])
    def handle_ReturnBook():
        if request.is_json:

            data = request.get_json()
            # (ISBN=data['ISBN'], username=data['username'], DueDate=data['DueDate'])
            ISBN = data['ISBN']
            username = data['username']

            user = Users.query.where(Users.username == username).all()
            if not user:
                return {"error": "No user by that username"}

            UserID = user[0].UserID

            books = BookCopies.query.where(BookCopies.ISBN == ISBN).all()

            if not books:
                return {"error": "Library does not have this book."}

            book_ids = [book.BookID for book in books]

            for book_id in book_ids:
                book = BorrowedBooks.query.where(BorrowedBooks.BookID == book_id).where(
                    BorrowedBooks.UserID == UserID).all()
                if book:
                    d = BorrowedBooks.query.where(BorrowedBooks.BookID == book_id).where(
                     BorrowedBooks.UserID == UserID).delete()
                    db.session.commit()
                    return {"message": "Book successfully returned."}

            return {"error": "User has not borrowed this book."}

    @app.route('/AvailableBookCopies', methods=['GET'])
    def handle_AvailableBookCopies():
        if request.is_json:

            data = request.get_json()
            ISBN = data['ISBN']

            books = BookCopies.query.where(BookCopies.ISBN == ISBN).all()

            if not books:
                return {"error": "Library does not have this book."}

            counter = 0
            borrowedBooks = []

            book_ids = [book.BookID for book in books]

            for book_id in book_ids:
                book = BorrowedBooks.query.where(BorrowedBooks.BookID == book_id).all()
                if book:
                    counter += 1
                    borrowedBooks.append(book[0])

            if len(borrowedBooks) == 0:
                return {"message": "There are {} copies of the book and they're all available".format(len(books))}
            else:
                availableBooks = len(books) - counter
                BorrowedBooksDetails = []

                # BorrowedBooksDetails = BorrowedBooks.query.where()order_by(BookModel.title).all()

                for book in borrowedBooks:
                    user = Users.query.where(Users.UserID == book.UserID).all()

                    BorrowedBooksDetails.append(
                        {
                            'username': user[0].username,
                            'Due Date': book.DueDate
                        })

                output_dict = {"Book Copies" : len(books), "Available Copies" : availableBooks, "Borrowed Book Details" : BorrowedBooksDetails}
                return output_dict






