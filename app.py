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

# choose_dishes_place_order
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
        db.create_all()
        db.session.commit()
        return app

if __name__ == "__main__":
    app=create_app()
    app.run(host='0.0.0.0',port=4545,debug=True)