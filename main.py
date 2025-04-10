from flask import Flask, request, render_template, redirect, session,flash
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer
import pymysql
import pickle

pickle_file_path =  "C:\\Projects\\SAP\\creditcardfraud_detection\\model_pickle"
with open(pickle_file_path, "rb") as file:
        model = pickle.load(file) 
    



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/creditcard_frod_detect'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_key'

db = SQLAlchemy(app)

class Signup(db.Model):
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    email = db.Column(String(50), nullable=False, unique=True)
    password = db.Column(String(50), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return redirect("/signup")

@app.route("/signup", methods=['GET', 'POST'])
def signup_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return "Email and Password are required", 400

        existing_user = Signup.query.filter_by(email=email).first()
        if existing_user:
            return "Email already registered!", 400

        entry = Signup(email=email, password=password)
        db.session.add(entry)
        db.session.commit()

        return redirect("/login")

    return render_template('signup.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Signup.query.filter_by(email=email, password=password).first()
        if user:
            session['user'] = email
            return redirect("/home")
        else:
            return "Invalid email or password", 400

    return render_template('login.html')

@app.route("/home")
def home():
      return render_template("index.html")

    


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        return redirect("/login")

    if request.method == 'POST':
        time = float(request.form.get('time'))
        amount = float(request.form.get('amount'))

        features = [float(request.form.get(f'feature{i}')) for i in range(1, 14)]

        X_input = pd.DataFrame([[time] + features + [amount]], 
                               columns=["Time","V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9","V10", "V26", "V27", "V28", "Amount"])

        X_test = model.predict(X_input)[0]  

        if X_test == 1:
            flash("⚠️ Fraudulent Transaction Detected!", "danger")
        else:
            flash("✅ Transaction is Safe.", "success")

        return redirect("/dashboard")  

    return render_template("dashboard.html")



@app.route("/logout")
def logout():
    session.pop('user', None)  
    return redirect("/login")  

with open(pickle_file_path, "rb") as file:
        model = pickle.load(file)  
    
if __name__ == "__main__":
    app.run(debug=True)


# import os
# import pickle
# import pandas as pd
# import pymysql
# from flask import Flask, request, render_template, redirect, session, flash
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import String, Integer
# from werkzeug.security import generate_password_hash, check_password_hash

# # Load the ML model
# pickle_file_path = "C:\\Users\\Sayli\\Downloads\\model_pickle"
# with open(pickle_file_path, "rb") as file:
#     model = pickle.load(file)

# # Initialize Flask app
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/creditcard_frod_detect'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.secret_key = 'secret_key'

# # Initialize Database
# db = SQLAlchemy(app)

# # Database Model
# class Signup(db.Model):
#     id = db.Column(Integer, primary_key=True, autoincrement=True)
#     email = db.Column(String(50), nullable=False, unique=True)
#     password = db.Column(String(255), nullable=False)  # Hashed passwords

# # Create tables
# with app.app_context():
#     db.create_all()

# # Routes
# @app.route("/")
# def index():
#     return redirect("/signup")

# @app.route("/signup", methods=['GET', 'POST'])
# def signup_page():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')

#         if not email or not password:
#             return "Email and Password are required", 400

#         existing_user = Signup.query.filter_by(email=email).first()
#         if existing_user:
#             return "Email already registered!", 400

#         hashed_password = generate_password_hash(password)
#         new_user = Signup(email=email, password=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()

#         return redirect("/login")

#     return render_template('signup.html')

# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')

#         user = Signup.query.filter_by(email=email).first()
#         if user and check_password_hash(user.password, password):
#             session['user'] = email
#             return redirect("/home")
#         else:
#             return "Invalid email or password", 400

#     return render_template('login.html')

# @app.route("/home")
# def home():
#     return render_template("index.html")

# @app.route("/dashboard", methods=['GET', 'POST'])
# def dashboard():
#     if 'user' not in session:
#         return redirect("/login")

#     if request.method == 'POST':
#         try:
#             time = float(request.form.get('time'))
#             amount = float(request.form.get('amount'))
#             features = [float(request.form.get(f'feature{i}')) for i in range(1, 14)]

#             X_input = pd.DataFrame([[time] + features + [amount]], 
#                                    columns=["Time", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10", "V26", "V27", "V28", "Amount"])
            
#             prediction = model.predict(X_input)[0]  

#             if prediction == 1:
#                 flash("⚠️ Fraudulent Transaction Detected!", "danger")
#             else:
#                 flash("✅ Transaction is Safe.", "success")

#         except Exception as e:
#             flash(f"Error: {e}", "danger")

#         return redirect("/dashboard")

#     return render_template("dashboard.html")

# @app.route("/logout")
# def logout():
#     session.pop('user', None)  
#     return redirect("/login")  

# # Run the Flask app
# if __name__ == "__main__":
#     app.run(debug=True)

