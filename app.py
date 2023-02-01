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

        db.create_all()
        db.session.commit()
        return app

if __name__ == "__main__":
    app=create_app()
    app.run(host='0.0.0.0',port=4545,debug=True)