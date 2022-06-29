from bookish.controllers.bookish import bookish_routes


def register_controllers(app):
    bookish_routes(app)
