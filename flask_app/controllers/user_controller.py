from flask_app import app
from flask import render_template,redirect,session,request,flash
from flask_app.models.user_model import User
from flask_app import bcrypt


#**********************LOGIN PAGE**********************

@app.route("/")
def login_page():
    return render_template("login.html")

#**********************REGISTER HANDLER**********************

@app.route("/register")
def register_page():
    return render_template('register.html')

@app.route("/register/user",methods=["POST"])
def register():
    if not User.validate_registration(request.form):
        return redirect('/')
    
    if request.form["password"]:
        hash = bcrypt.generate_password_hash(request.form['password'])


    data = {
        **request.form,
        "password" : hash
    }

    print(request.form)

    user_in_db = User.get_user_email(request.form)

    if user_in_db:
        flash("User already exists","register")
        return redirect("/")

    User.created_user(data)
    logged_in_user = User.get_user_email(data)

    session["email"] = logged_in_user.email
    session["uid"] = logged_in_user.id
    session["username"] = logged_in_user.first_name + ' ' + logged_in_user.last_name
    return redirect("/dashboard")


#**********************LOGIN HANDLER**********************

@app.route("/login",methods=["POST"])
def login():
    logged_in_user = User.validate_login(request.form)

    if not logged_in_user:
        return redirect("/")
    
    session["uid"] = logged_in_user.id
    session["username"] = logged_in_user.first_name + ' ' + logged_in_user.last_name
    session["email"] = logged_in_user.email
    return redirect("/dashboard")

@app.route("/guest")
def guest_login():
    session["username"] = "Guest"
    session["email"] = "Guest"
    session["cart"]  = []
    return redirect("/dashboard")


#**********************LOGOUT**********************

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")