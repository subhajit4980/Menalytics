from flask import Flask, jsonify, request
from flask_cors import CORS
from config import db, SECRET_KEY
from os import environ, path, getcwd
from dotenv import load_dotenv
from datetime import datetime,date
import pytz
from sqlalchemy.orm import sessionmaker
from model.customer import Customer
from model.add_items import Add_items
from model.customer_ordered_record import Customer_ordered_record
from model.get_customer_ordered_dishes import Get_customer_ordered_dishes
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
        #  customer signup part
        @app.route('/customer_signup', methods=['POST'])
        def customer_signup():
            data = request.form.to_dict(flat=True)
            print(data)
            new_customer = Customer(
                username=data["username"],
                password=data['password'],
                name=data['name'],
                email=data['email'],
                phone=data['phone'],
                address=data['address']
            )
            try:
                users=Customer.query.all()
                usernamelist=[user.username for user in users]
                if new_customer.username  not in usernamelist:
                    db.session.add(new_customer)
                    db.session.commit()
                else:
                    return jsonify("username already in used")
            except:
                return jsonify("some thing went wrong")
            return jsonify(msg="Signup Successfully")
# customer signin part
        @app.route("/customer_signin", methods=['POST'])
        def customer_signin():
            if request.method=="POST":
                    c_username=request.form['username']
                    c_password=request.form['password']
                    users=Customer.query.all()
                    for user in users:
                        if user.username==c_username and user.password==c_password :
                            user_idx=user.id
                            response={
                                "massage":"Login successful",
                                "user_id": user_idx
                            }
                            return response
                        else:
                            continue
            return "user doesn't exists"
        #  restaurant signup part
        @app.route("/restaurants_signup",methods=['POST'])
        def restaurants_signup():
            data = request.form.to_dict(flat=True)
            print(data)
            new_restaurant = Restaurant(
                username = data['username'],
                password = data['password'],
                name = data['name'],
                phone_number = data['phone_number'],
                email = data['email'],
                address = data['address'],
            )
            try:
                restaurants=Restaurant.query.all()
                usernamelist=[restaurant.username for restaurant in restaurants]
                if new_restaurant.username not in usernamelist:
                    db.session.add(new_restaurant)
                    db.session.commit()
                    # return jsonify(msg="username already in used, kindly try again!!")
                else:
                    return jsonify("username already in used, kindly try again!!")
            except:
                return jsonify("SOMETHING WENT WRONG!!") 
            return jsonify(msg="Signup Successfully")
#restaurant signin
        @app.route("/restaurants_signin", methods=["POST"])
        def restaurants_signin():
            if request.method=="POST":
                c_username=request.form['username']
                c_password=request.form['password']
                users=Restaurant.query.all()
                for restaurant in users:
                    if restaurant.username==c_username and restaurant.password==c_password :
                        user_idx=restaurant.id
                        response={
                            "massage":"Login successful",
                            "user_id": user_idx
                        }
                        return response
                    else:
                        continue
                return jsonify(msg="Unvalid username or password. Please try again!!")

# #choose_dishes_place_order
        @app.route("/choose_dishes_place_order", methods=["GET", "POST"])
        def choose_dishes_place_order():
            username = request.args.get('username')
            customers = Customer.query.filter_by(username=username).first()
            if customers is not None:
                order_rec = request.get_json()
                for data in order_rec["data"]:
                    record = Customer_ordered_record(

                        restaurant_name=data['restaurant_name'],
                        dish_name=data['dish_name'],
                        quantity=data['quantity'],
                        price=0,
                        Total_price=0,
                        purchased_date=str(datetime.now(pytz.timezone("Asia/Kolkata"))),
                        delivery_address=data["delivery_address"],
                        customer_username=customers.username
                    )
                    restaurant_data = Add_items.query.filter_by(restaurant_name=record.restaurant_name).first()  
                    dish=Add_items.query.filter_by(item_name=record.dish_name).first()
                    if dish is not None and restaurant_data is not None:
                        record.price=dish.price
                        record.Total_price=record.price * record.quantity
                        if  record.restaurant_name == restaurant_data.restaurant_name:
                            if record.quantity <= restaurant_data.quantity and record.dish_name ==restaurant_data.item_name:
                                dish.quantity-=record.quantity
                                if dish.quantity==0:
                                    db.session.delete(dish)
                                    db.session.commit()
                                else:
                                    db.session.add(dish)
                                db.session.add(record)
                            else:
                                return jsonify(f"{record.dish_name} not available or this quantity is not available")
                        else:
                            return jsonify("Wrong restaurant Name: ", record.restaurant_name)
                        
                        order=Get_customer_ordered_dishes(
                            restaurant_name=record.restaurant_name,
                            customer_name=customers.name,
                            item_name=record.dish_name,
                            quantity=record.quantity,
                            address=customers.address,
                            phone=customers.phone,
                            order_time=str(datetime.now(pytz.timezone("Asia/Kolkata")))
                        )
                        db.session.add(order)
                    else:
                        return jsonify("dish or restaurant choosen wrong !!!!")
                db.session.commit()
                return jsonify("Order successful. Payment should be done in cash to the delivery partner")    
            else:
                return jsonify("user is not authorized")

        @app.route("/check_order_history",methods=["GET", "POST"])
        def check_order_history():
            customer_username = request.form["username"]
            customer_order=Customer_ordered_record.query.all()
            order_list={}
            for order in customer_order:
                if order.customer_username ==customer_username:
                    customer={}
                    customer["restaurant_name"]=order.restaurant_name
                    customer["dish_name"]=order.dish_name
                    customer["quantity"]=order.quantity
                    customer["price"]=order.price
                    customer["Total_price"]=order.Total_price
                    customer["delivery_address"]=order.delivery_address
                    order_list[order.purchased_date]=customer
            return jsonify("you didn't order anything" if len(order_list)==0 else order_list)
    
        @app.route("/delivery_order", methods=["GET", "POST"])
        def delivery_order():
            restaurant_name=request.form["restaurant_name"]
            customer_order=Get_customer_ordered_dishes.query.all()
            for order in customer_order:
                if order.restaurant_name==restaurant_name:
                    db.session.delete(order)
                    db.session.commit()
                    return jsonify(f"{order.item_name} delivered to {order.customer_name} successfully !")
            return jsonify("no delivery pending")
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
        @app.route('/add_items_details', methods=['POST'])
        def add_items():
            username = request.args.get('username')
            restaurant_data = Restaurant.query.filter_by(username=username).first()
            if restaurant_data is not None:
                items_data = request.get_json()
                for data in items_data["data"]:
                    new_items = Add_items(
                        item_name=data["item_name"],
                        description=data["description"],
                        price=data["price"],
                        cooking_time=data["cooking_time"],
                        quantity=data["quantity"],
                        restaurant_signup_id=restaurant_data.id,
                        restaurant_name=restaurant_data.name
                    )
                    item=Add_items.query.filter_by(item_name=new_items.item_name).first()
                    if item is not None and item.restaurant_signup_id==new_items.restaurant_signup_id:
                        new_items.quantity+=(int)(item.quantity)
                        db.session.delete(item)
                    db.session.add(new_items)
                    db.session.commit()
                    print(items_data)
                return jsonify(msg="Items Details Added Successfully")
            else:
                return jsonify(msg="wrong username")

        @app.route("/get_customer_order_details",methods=["GET", "POST"])
        def get_order_details():
            restaurant_name = request.form["restaurant_name"]
            customer_order=Get_customer_ordered_dishes.query.all()
            order_list={}
            for order in customer_order:
                if order.restaurant_name==restaurant_name:
                    customer={}
                    customer["customer_name"]=order.customer_name
                    customer["dish_name"]=order.item_name
                    customer["quantity"]=order.quantity
                    customer["phone"]=order.phone
                    customer["delivery_address"]=order.address
                    order_list[order.order_time]=customer
            return jsonify("No dishes ordered" if len(order_list)==0 else order_list)

        db.create_all()
        db.session.commit()
        return app
if __name__ == "__main__":
    app=create_app()
    app.run(host='0.0.0.0',port=4545,debug=True)