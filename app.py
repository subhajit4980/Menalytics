from flask import Flask, jsonify, request
from flask_cors import CORS
from config import db, SECRET_KEY
from os import environ, path, getcwd
from dotenv import load_dotenv
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
                r_username=request.form['username']
                r_password=request.form['password']
                users=Restaurant.query.all()
                for restaurant in users:
                    if restaurant.username==r_username and restaurant.password==r_password :
                        user_idx=restaurant.id
                        response={
                            "massage":"Login successful",
                            "user_id": user_idx
                        }
                        return response
                    else:
                        continue
                return jsonify(msg="Unvalid username or password. Please try again!!")

        db.create_all()
        db.session.commit()
        return app

if __name__ == "__main__":
    app=create_app()
    app.run(host='0.0.0.0',port=4545,debug=True)