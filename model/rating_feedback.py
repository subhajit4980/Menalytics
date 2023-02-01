from config import db

class Rating_feedback(db.Model):
    _tablename_ = 'rating_feedback'
    id = db.Column(db.Integer, primary_key=True)
    restaurant_name = db.Column(db.String(200), nullable=False)
    customer_name = db.Column(db.String(200), nullable=False)
    item_name = db.Column(db.String(200), nullable=False)
    item_rating = db.Column(db.Float, nullable=False)
    item_feedback = db.Column(db.String(300),nullable=False)