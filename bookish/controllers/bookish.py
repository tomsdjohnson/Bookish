from flask import request
from bookish.models.example import BookModel, BookCopies, BorrowedBooks, Users
from bookish.models import db
import random

def bookish_routes(app):
    @app.route('/healthcheck')
    def health_check():
        return {"status": "OK"}

    @app.route('/AddBook', methods=['POST'])
    def handle_AddBook():
        if request.is_json:

            data = request.get_json()
            new_book_model = BookModel(ISBN=data['ISBN'], title=data['title'], author=data['author'])
            db.session.add(new_book_model)

            # Add new copies
            for _ in range(data['copies']):
                new_book_copy = BookCopies(ISBN=data['ISBN'])
                db.session.add(new_book_copy)

            db.session.commit()

            return {"message": "New book has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    @app.route('/GetBooks', methods=['GET'])
    def handle_GetBooks():
        books = BookModel.query.order_by(BookModel.title).all()
        output = [
            {
                'ISBN': book.ISBN,
                'title': book.title,
                'author': book.author
            } for book in books]
        return {"Books": output}

    @app.route('/NewUser', methods=['POST'])
    def handle_NewUser():
        if request.is_json:

            data = request.get_json()
            inputUsername = data['username']

            if inputUsername in [user.username for user in Users.query.all()]:
                return {"message": "Username already taken"}
            else:
                new_user = Users(username=inputUsername, password=data['password'])
                db.session.add(new_user)
                db.session.commit()

                return {"message": "New user has been created successfully."}

        else:
            return {"error": "The request payload is not in JSON format"}

    @app.route('/SearchBookByTitle', methods=['GET'])
    def handle_SearchBookByTitle():
        if request.is_json:

            data = request.get_json()
            inputTitle = data['title']

            books_with_title = BookModel.query.where(BookModel.title == inputTitle).all()
            if not books_with_title:
                return {"error": "No books with that title"}
            output = [
                {
                    'ISBN': book.ISBN,
                    'title': book.title,
                    'author': book.author
                } for book in books_with_title]
            return {"Books": output}

        else:
            return {"error": "The request payload is not in JSON format"}

    @app.route('/SearchBookByAuthor', methods=['GET'])
    def handle_SearchBookByAuthor():
        if request.is_json:

            data = request.get_json()
            inputAuthor = data['author']

            books_with_author = BookModel.query.where(BookModel.author == inputAuthor).all()
            if not books_with_author:
                return {"error": "No books by that author"}
            output = [
                {
                    'ISBN': book.ISBN,
                    'title': book.title,
                    'author': book.author
                } for book in books_with_author]
            return {"Books": output}

        else:
            return {"error": "The request payload is not in JSON format"}

    @app.route('/BorrowBook', methods=['POST'])
    def handle_BorrowBook():
        if request.is_json:

            data = request.get_json()
            inputISBN = data['ISBN']
            inputUsername = data['username']
            inputDueDate = data['DueDate']

            users_with_username = Users.query.where(Users.username == inputUsername).all()
            if not users_with_username:
                return {"error": "No user by that username"}

            if len(users_with_username) > 1:
                return {"error": "Multiple users by that username"}

            UserID = users_with_username[0].UserID

            bookCopies_with_ISBN = BookCopies.query.where(BookCopies.ISBN == inputISBN).all()

            if not bookCopies_with_ISBN:
                return {"error": "Library does not have this book."}

            book_ids_with_ISBN = [book.BookID for book in bookCopies_with_ISBN]

            # Check if user already has borrowed this book
            for book_id in book_ids_with_ISBN:
                book = BorrowedBooks.query.where(BorrowedBooks.BookID == book_id).where(BorrowedBooks.UserID == UserID).all()
                if book:
                    return {"error": "User has already borrowed this book."}

            #Check if any book copy is available and borrow it
            for book_id in book_ids_with_ISBN:
                book = BorrowedBooks.query.where(BorrowedBooks.BookID == book_id).all()
                if not book:
                    new_borrowed_book = BorrowedBooks(BookID=book_id, UserID=UserID, DueDate = inputDueDate)
                    db.session.add(new_borrowed_book)
                    db.session.commit()
                    return {"message": "Book successfully borrowed."}
            return {"error": "All books are borrowed."}

        else:
            return {"error": "The request payload is not in JSON format"}

    @app.route('/ReturnBook', methods=['POST'])
    def handle_ReturnBook():
        if request.is_json:

            data = request.get_json()
            inputISBN = data['ISBN']
            inputUsername = data['username']


            users_with_username = Users.query.where(Users.username == inputUsername).all()
            if not users_with_username:
                return {"error": "No user by that username"}

            if len(users_with_username) > 1:
                return {"error": "Multiple users by that username"}

            #Get UserID
            UserID = users_with_username[0].UserID

            books_with_ISBN = BookCopies.query.where(BookCopies.ISBN == inputISBN).all()

            if not books_with_ISBN:
                return {"error": "Library does not have this book."}

            book_ids = [book.BookID for book in books_with_ISBN]

            #Search for BookID borrowed by user and return it
            for book_id in book_ids:
                book = BorrowedBooks.query.where(BorrowedBooks.BookID == book_id).where(
                    BorrowedBooks.UserID == UserID).all()
                if book:
                    #Delete BorrowedBooks entry
                    d = BorrowedBooks.query.where(BorrowedBooks.BookID == book_id).where(
                     BorrowedBooks.UserID == UserID).delete()
                    db.session.commit()
                    return {"message": "Book successfully returned."}

            return {"error": "User has not borrowed this book."}

        else:
            return {"error": "The request payload is not in JSON format"}

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
        else:
            return {"error": "The request payload is not in JSON format"}

    @app.route('/BooksBorrowedByUser', methods=['GET'])
    def handle_BooksBorrowedByUser():
        if request.is_json:

            data = request.get_json()
            username = data['username']

            usernames = Users.query.where(Users.username == username).all()

            if not usernames:
                return {"error": "User does not exist."}

            UserID = usernames[0].UserID
            BorrowedBooksByUserDetails = []

            borrowed_books = BorrowedBooks.query.where(BorrowedBooks.UserID == UserID).all()

            for borrowed_book in borrowed_books:
                BookID = borrowed_book.BookID
                ISBN = BookCopies.query.where(BookCopies.BookID == BookID).all()[0].ISBN
                title = BookModel.query.where(BookModel.ISBN == ISBN).all()[0].title

                BorrowedBooksByUserDetails.append(
                    {
                        'title': title,
                        'Due Date': borrowed_book.DueDate
                    })

            if not borrowed_books:
                return {"message": "User has not borrowed any books."}
            else:
                return {"Borrowed Books": BorrowedBooksByUserDetails}
        else:
            return {"error": "The request payload is not in JSON format"}

    @app.route('/EditBook', methods=['POST'])
    def handle_EditBook():
        if request.is_json:

            data = request.get_json()
            output_messages = []
            counter = 0

            book = BookModel.query.where(BookModel.ISBN == data['ISBN']).all()
            if not book:
                return {"error": "Book does not exist."}

            book = book[0]
            if 'title' in data:
                book.title = data['title']
                output_messages.append({"message": "Title successfully changed."})
            if 'author' in data:
                book.author = data['author']
                output_messages.append({"message": "Author successfully changed."})
            if 'copies' in data:

                if data['copies'] < 0:
                    return {"error": "Not a valid number of copies"}


                books = BookCopies.query.where(BookCopies.ISBN == data['ISBN']).all()
                book_ids = [book.BookID for book in books]
                current_copies = len(book_ids)
                borrowed_book_ids = []

                if data['copies'] == current_copies:
                    output_messages.append({"message": "Already have that number of copies."})
                    return {"output messages" : output_messages}

                for book_id in book_ids:
                    borrowed_books = BorrowedBooks.query.where(BorrowedBooks.BookID == book_id).all()

                    if borrowed_books:
                        counter += 1
                        borrowed_book_ids.append(book_id)

                if data['copies'] < (current_copies - counter):
                    output_messages.append({"error": "Can't remove a borrowed book."})
                    return {"output messages": output_messages}

                if data['copies'] > current_copies:
                    for x in range(data['copies'] - current_copies):
                        new_book_copy = BookCopies(ISBN=data['ISBN'])
                        db.session.add(new_book_copy)
                    output_messages.append({"message": "{} copies added".format(data['copies'] - current_copies)})

                if data['copies'] < current_copies:
                    book_ids_set = set(book_ids)
                    borrowed_book_ids_set = set(borrowed_book_ids)

                    unborrowed_book_ids = list(book_ids_set.difference(borrowed_book_ids_set))

                    for unborrowed_book_id in unborrowed_book_ids[:(current_copies - data['copies'])]:
                        d = BookCopies.query.where(BookCopies.BookID == unborrowed_book_id).delete()
                    output_messages.append({"message": "{} copies removed".format(current_copies - data['copies'])})

                if data['copies'] == 0:
                    d = BookModel.query.where(BookModel.ISBN == data['ISBN']).delete()
                    output_messages.append({"message": "Book deleted."})

            db.session.commit()

            return {"output messages": output_messages}

        else:
            return {"error": "The request payload is not in JSON format"}

    @app.route('/AddBooksCsv', methods=['POST'])
    def handle_AddBooksCsv():
        if 'file' not in request.files:
            return {"error": "csv file not included"}

        file = request.files['file']

        with open("file.csv", "r") as book_file:

            for book_input in book_file.readlines()[1:]:
                book_data = book_input.split(",")[0:3]
                new_book_model = BookModel(ISBN=book_data[0], title=book_data[1], author=book_data[2])

                for x in range(random.randint(1, 8)):
                    new_book_copy = BookCopies(ISBN=book_data[0])
                    db.session.add(new_book_copy)

                db.session.add(new_book_model)

                db.session.commit()

        return {"message": "successfully added books from csv"}


