from flask import Flask, jsonify, request
from flask_cors import CORS
from config import db, SECRET_KEY
from os import environ, path, getcwd
from dotenv import load_dotenv
from datetime import datetime,date
import pytz
from sqlalchemy.orm import sessionmaker
from model.add_items import Add_items
from model.restaurant import Restaurant
from model.rating_feedback import Rating_feedback

load_dotenv(path.join(getcwd(),'.env'))

def create_app():
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]=environ.get('DB_URI')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = False
    app.secret_key = SECRET_KEY
    db.init_app(app)
    print("DB Initialized Sucessfully")
    CORS(app)
    with app.app_context():
        @app.route('/choose_restaurant', methods=['POST'])
        def choose_restaurant():
            restaurant_name = request.form["restaurant_name"]

            #* taking the restarant details
            restaurant_data = Add_items.query.all()
            
            #* to show the dishes
            restaurant_items = {
                "Restaurant name": restaurant_name
            }
            list_items = []
            for i in restaurant_data:
                if(restaurant_name == i.restaurant_name):
                    list_items.append(i.item_name)
                    rating_feedback_data = Rating_feedback.query.all()
                    list_dishes = []
                    for item in list_items:
                        rating = 0
                        count = 0
                        for feedback in rating_feedback_data:
                            if(item == feedback.item_name):
                                rating += feedback.item_rating
                                count += 1
                        data = {
                            "Item name": item,
                            "Quantity": Add_items.query.filter_by(item_name=item).first().quantity,
                            "Item rating": rating/count if count > 0 else "Not rated yet",
                            "No of reviews": count
                        }
                        list_dishes.append(data)
                        restaurant_items["The Dishes"] = list_dishes
                else:
                    continue
            return jsonify(f"Sorry, {restaurant_name} is not available." if len(restaurant_items)==1 else restaurant_items )
        
        @app.route('/give_rating_feedback', methods=['POST'])
        def give_rating_feedback():
            rating_feedback_data = request.get_json()
            new_rating_feedback = Rating_feedback(
                restaurant_name = rating_feedback_data["restaurant name"],
                customer_name = rating_feedback_data["customer name"],
                item_name = rating_feedback_data["item name"],
                item_rating = rating_feedback_data["item rating"],
                item_feedback = rating_feedback_data["item feedback"]
            )
            db.session.add(new_rating_feedback)
            db.session.commit()
            print(rating_feedback_data)
            return jsonify(msg="Thanks for your feedback")

        db.create_all()
        db.session.commit()
        return app

if __name__ == "__main__":
    app=create_app()
    app.run(host='0.0.0.0',port=4545,debug=True)