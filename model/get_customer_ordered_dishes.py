from config import db

class Get_customer_ordered_dishes(db.Model):
    _tablename_ = 'get_customer_ordered_dishes'
    id = db.Column(db.Integer, primary_key=True)
    # restaurant_id = db.Column(db.String(255), nullable=False)
    restaurant_name = db.Column(db.String(255), nullable=False)
    customer_name = db.Column(db.String(255), nullable=False)
    item_name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    order_time=db.Column(db.String(255), nullable=False)
    # restaurant_username = db.Column(db.Integer, db.ForeignKey('restaurant.username'))