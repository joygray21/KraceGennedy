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
        return '<Worker %r>' % (self.name)


# class EmailHistory(db.Model):
#     day = db.Column(db.Integer, primary_key=True, autoincrement=False)
#     rainyEmailsSent = db.Column(db.Boolean)
#     sunnyEmailsSent = db.Column(db.Boolean)
#     ITEmailsSent = db.Column(db.Boolean)
### would need to adjust to consider cities

#     def __init__(self, day, rainyEmailsSent, sunnyEmailsSent, ITEmailsSent):
#         self.day = day
#         self.rainyEmailsSent = rainyEmailsSent
#         self.sunnyEmailsSent = sunnyEmailsSent
#         self.ITEmailsSent = ITEmailsSent
    
#     def __repr__(self):
#         return '<EmailHistory %r>' % (self.day)
