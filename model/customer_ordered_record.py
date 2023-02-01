from config import db

class Customer_ordered_record(db.Model):
    __tablename__ = 'customer_ordered_record'
    id= db.Column(db.Integer, primary_key=True)
    restaurant_name=db.Column(db.String(200),nullable=False)
    dish_name=db.Column(db.String(200),nullable=False)
    quantity=db.Column(db.Integer,nullable=False)
    delivery_address=db.Column(db.String(400),nullable=False)
    Total_price=db.Column(db.Integer,nullable=False)
    purchased_date=db.Column(db.String(50),nullable=False)
    customer_username = db.Column(db.String(200), db.ForeignKey('customer.username'))
    price=db.Column(db.Integer,nullable=False)

