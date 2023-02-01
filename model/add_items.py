from config import db

class Add_items(db.Model):
    _tablename_ = 'add_items'
    id = db.Column(db.Integer, primary_key=True)
    restaurant_name = db.Column(db.String(255), nullable=False)
    item_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    cooking_time = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    restaurant_signup_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    # customer_ordered_record=db.relationship('Customer_ordered_record',backref='add_items')