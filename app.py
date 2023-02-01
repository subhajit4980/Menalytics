from flask import Flask, jsonify, request
from flask_cors import CORS
from config import db, SECRET_KEY
from os import environ, path, getcwd
from dotenv import load_dotenv
from model.add_items import Add_items
from model.restaurant import Restaurant
from model.get_customer_ordered_dishes import Get_customer_ordered_dishes

load_dotenv(path.join(getcwd(),'.env'))

def create_app():
    app=Flask(_name_)
    app.config["SQLALCHEMY_DATABASE_URI"]=environ.get('DB_URI')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = False
    app.secret_key = SECRET_KEY
    db.init_app(app)
    print("DB Initialized Sucessfully")
    CORS(app)
    with app.app_context():
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

if _name_ == "_main_":
    app=create_app()
    app.run(host='0.0.0.0',port=4545,debug=True)