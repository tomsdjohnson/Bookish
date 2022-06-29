from bookish.app import db


class Example(db.Model):
    # This sets the name of the table in the database
    __tablename__ = 'Test'

    # Here we outline what columns we want in our database
    id = db.Column(db.Integer, primary_key=True)
    data1 = db.Column(db.String())
    data2 = db.Column(db.String())

    def __init__(self, data1, data2):
        self.data1 = data1
        self.data2 = data2

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'data1': self.data1,
            'data2': self.data2
        }
