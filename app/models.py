from . import db

class Worker(db.Model):
    __tablename__ = 'workers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160))
    street = db.Column(db.String(80))
    city = db.Column(db.String(80))
    role = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)

    def __init__(self, name, street, city, role, email):
        self.name = first_name
        self.street = street
        self.city = city
        self.role = role
        self.email = email

    
    def __repr__(self):
        return '<User %r>' % (self.name)
