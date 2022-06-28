from flask import Flask, request
from kuppa.models.book import Book


def bookish_routes(app):
    @app.route('/books', methods=['POST', 'GET'])
    def get_books():
        if request.method == 'GET':
            books = Book.query.all()
            results = [
                {
                    'id': book.id,
                    'name': book.name,
                    'author': book.author,
                    'published': book.published
                } for book in books]

            return {"count": len(results), "cars": results}
