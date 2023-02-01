from config import db

class Restaurant(db.Model):
    _tablename_ = 'restaurant'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255),unique=True, nullable=False)
    name = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone_number = db.Column(db.String(150), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255),nullable=False)
    add_items=db.relationship('Add_items',backref='restaurant')