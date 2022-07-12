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
            input_ISBN = data['ISBN']
            input_title = data['title']
            input_author = data['author']

            #Check book doesn't already exist
            books_with_ISBN = BookModel.query.where(BookModel.ISBN == input_ISBN).all()
            if books_with_ISBN:
                return {"error": "Book with ISBN {} is already in the database.".format(input_ISBN)}

            new_book_model = BookModel(ISBN=input_ISBN, title=input_title, author=input_author)
            db.session.add(new_book_model)

            # Add new copies
            for _ in range(data['copies']):
                new_book_copy = BookCopies(ISBN=input_ISBN)
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

    # Search Book where input is title
    @app.route('/SearchBookByTitle', methods=['GET'])
    def handle_SearchBookByTitle():

        data = request.headers
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

    # Search Book where input is author
    @app.route('/SearchBookByAuthor', methods=['GET'])
    def handle_SearchBookByAuthor():

        data = request.headers
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

    # Search Book where input is substring of title or author
    @app.route('/DynamicSearchBook', methods=['GET'])
    def handle_DynamicSearchBook():

        data = request.headers

        if 'title' in data:

            inputTitle = data['title']

            search = "%{}%".format(inputTitle)
            books_with_title = BookModel.query.filter(BookModel.title.ilike(search)).order_by(
                BookModel.title.asc()).all()

            if not books_with_title:
                return {"error": "No books with that title"}
            output = [
                {
                    'ISBN': book.ISBN,
                    'title': book.title,
                    'author': book.author
                } for book in books_with_title]

        elif 'author' in data:

            inputAuthor = data['author']

            search = "%{}%".format(inputAuthor)
            books_with_author = BookModel.query.filter(BookModel.author.ilike(search)).order_by(
                BookModel.title.asc()).all()

            if not books_with_author:
                return {"error": "No books with that author"}
            output = [
                {
                    'ISBN': book.ISBN,
                    'title': book.title,
                    'author': book.author
                } for book in books_with_author]

        else:

            return {"error": "you didn't input the title or author."}

        return {"Books": output}

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

        data = request.headers
        inputISBN = data['ISBN']

        copies_with_ISBN = BookCopies.query.where(BookCopies.ISBN == inputISBN).all()

        if not copies_with_ISBN:
            return {"error": "Library does not have this book."}

        borrowed_copies_counter = 0
        borrowed_copies = []

        book_ids = [book.BookID for book in copies_with_ISBN]

        for book_id in book_ids:
            book = BorrowedBooks.query.where(BorrowedBooks.BookID == book_id).all()
            if book:
                borrowed_copies_counter += 1
                borrowed_copies.append(book[0])

        if len(borrowed_copies) == 0:
            return {"message": "There are {} copies of the book and they're all available".format(len(copies_with_ISBN))}
        else:
            availableCopies = len(copies_with_ISBN) - borrowed_copies_counter
            BorrowedBooksDetails = []

            for copy in borrowed_copies:
                user = Users.query.where(Users.UserID == copy.UserID).all()

                BorrowedBooksDetails.append(
                    {
                        'username': user[0].username,
                        'Due Date': copy.DueDate
                    })

            output_dict = {"Book Copies": len(copies_with_ISBN), "Available Copies": availableCopies, "Borrowed Book Details": BorrowedBooksDetails}
            return output_dict

    @app.route('/BooksBorrowedByUser', methods=['GET'])
    def handle_BooksBorrowedByUser():

        data = request.headers
        inputUsername = data['username']

        users_with_username = Users.query.where(Users.username == inputUsername).all()

        if not users_with_username:
            return {"error": "User does not exist."}
        if len(users_with_username) > 1:
            return {"error": "Multiple users by that username"}

        UserID = users_with_username[0].UserID
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

    @app.route('/EditBook', methods=['POST'])
    def handle_EditBook():
        if request.is_json:

            data = request.get_json()
            input_ISBN = data['ISBN']
            output_messages = []

            books_with_ISBN = BookModel.query.where(BookModel.ISBN == input_ISBN).all()
            if not books_with_ISBN:
                return {"error": "Book does not exist."}

            book_with_ISBN = books_with_ISBN[0]
            
            if 'title' in data:
                book_with_ISBN.title = data['title']
                db.session.commit()
                output_messages.append({"message": "Title successfully changed."})
                
            if 'author' in data:
                book_with_ISBN.author = data['author']
                db.session.commit()
                output_messages.append({"message": "Author successfully changed."})
                
            if 'copies' in data:
                input_copies = data['copies']
                
                if input_copies < 0:
                    output_messages.append({"error": "Not a valid number of copies"})
                    return {"output messages": output_messages}

                copies_with_ISBN = BookCopies.query.where(BookCopies.ISBN == input_ISBN).all()
                book_ids = [book.BookID for book in copies_with_ISBN]
                
                current_copies = len(book_ids)
               
                if input_copies == current_copies:
                    output_messages.append({"message": "Already have that number of copies."})
                    return {"output messages" : output_messages}

                borrowed_book_ids = []
                borrowed_copies_counter_ = 0
                
                #Count borrowed copies and append them
                for book_id in book_ids:
                    borrowed_books = BorrowedBooks.query.where(BorrowedBooks.BookID == book_id).all()
                    if borrowed_books:
                        borrowed_copies_counter_ += 1
                        borrowed_book_ids.append(book_id)
                
                #Trying to remove more copies than are not borrowed
                if input_copies < (current_copies - borrowed_copies_counter_):
                    output_messages.append({"error": "Can't remove a borrowed book."})
                    return {"output messages": output_messages}

                #Trying to add more copies than currently
                if input_copies > current_copies:
                    for _ in range(input_copies - current_copies):
                        new_book_copy = BookCopies(ISBN=input_ISBN)
                        db.session.add(new_book_copy)
                    db.session.commit()
                    output_messages.append({"message": "{} copies added".format(input_copies - current_copies)})

                # Trying to remove unborrowed copies
                if input_copies < current_copies:
                    book_ids_set = set(book_ids)
                    borrowed_book_ids_set = set(borrowed_book_ids)

                    #Get IDs of unborrowed copies
                    unborrowed_book_ids = list(book_ids_set.difference(borrowed_book_ids_set))

                    for unborrowed_book_id in unborrowed_book_ids[:(current_copies - input_copies)]:
                        BookCopies.query.where(BookCopies.BookID == unborrowed_book_id).delete()
                        db.session.commit()
                    output_messages.append({"message": "{} copies removed".format(current_copies - input_copies)})

                #If all copies are removed, remove also the BookModel
                if input_copies == 0:
                    BookModel.query.where(BookModel.ISBN == input_ISBN).delete()
                    db.session.commit()
                    output_messages.append({"message": "Book deleted."})

            return {"output messages": output_messages}
        else:
            return {"error": "The request payload is not in JSON format"}

    @app.route('/AddBooksCsv', methods=['POST'])
    def handle_AddBooksCsv():
        if 'file' not in request.files:
            return {"error": "csv file not included"}

        file = request.files['file']

        with open(file.filename, "r") as book_file:

            output_message = []

            for book_input in book_file.readlines()[1:]:
                book_data = book_input.split(",")[0:3]

                books_with_ISBN = BookModel.query.where(BookModel.ISBN == book_data[0]).all()
                if books_with_ISBN:
                    output_message.append({"error": "Book with ISBN {} is already in the database.".format(book_data[0])})
                    continue

                new_book_model = BookModel(ISBN=book_data[0], title=book_data[1], author=book_data[2])

                #Add a random amount of copies to populate the database
                for _ in range(random.randint(1, 8)):
                    new_book_copy = BookCopies(ISBN=book_data[0])
                    db.session.add(new_book_copy)

                db.session.add(new_book_model)

                db.session.commit()

        if output_message:
            return {"message": "Added books from csv but some entries were already in the database.",
                    "errors": output_message}
        else:
            return {"message": "successfully added books from csv"}


