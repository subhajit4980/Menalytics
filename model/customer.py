from config import db

class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name=db.Column(db.String(150),nullable=False)
    email=db.Column(db.String(150),nullable=False)
    phone=db.Column(db.String(150),nullable=False)
    address=db.Column(db.String(350),nullable=False)
    customer_ordered_record=db.relationship('Customer_ordered_record',backref='customer')