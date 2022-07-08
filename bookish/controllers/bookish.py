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
