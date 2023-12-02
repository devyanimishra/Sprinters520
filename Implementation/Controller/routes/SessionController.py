import re
from werkzeug.security import generate_password_hash, check_password_hash
from flask import (request, flash, redirect, url_for, session, render_template)


from Controller.Helper import login_required
from Model.DatabaseClient import DatabaseClient

class SessionController:

    def __init__(self):
        self.dbClient = DatabaseClient()

    def register(self):
        """
        Get patient's username from the form, check if it already exists in
        the database. If it does, flash a message to the user and redirect to
        registration page. Check if passwords match and in the correct format.
        Save user in the database, put user into a session cookie and redirect
        to profile page.
        """
        actor = str(request.args.get('actor'))
        print("hellllooo", actor, type(actor))
        collection = self.dbClient.db[actor]

        print("We are in register", request.method)
        if request.method == "POST":
            
            # check if username already exists in db
            existing_user = collection.find_one(
                {"username": request.form.get("username").lower()})
            
            if existing_user:
                flash("Username already exists", "danger")
                return redirect(url_for("register"))
            
            # check if passwords match
            password = request.form.get("password")
            confirm_password = request.form.get("confirm-password")
            
            if password != confirm_password:
                flash("Your passwords don't match", "danger")
                return redirect(url_for("register"))
            
            is_digit = re.compile(r"[0-9]")
            is_lower = re.compile(r"[a-z]")
            is_upper = re.compile(r"[A-Z]")

            if is_digit.search(password) is None or \
                is_lower.search(password) is None or \
                    is_upper.search(password) is None:
                return redirect(url_for("register"))
            
            register_user = {
                "fullname": request.form.get("fullname").title(),
                "username": request.form.get("username").lower(),
                "password": generate_password_hash(request.form.get("password")),
                "email": request.form.get("email"),
                "Contact": int(request.form.get("contact")),
                "Date_of_Birth": request.form.get("dob"),
                "Gender": request.form.get("gender"),
                "is_admin": False,
            }
            
            if actor == "patient":
                register_user["Medical History"] = request.form.get("medicalHistory")
                register_user["actor"] = "patient"
                register_user["_id"] = "P"+str(hash(register_user["Date_of_Birth"]+str(register_user["Contact"])))[1:7]
            elif actor == "doctor":
                register_user["Fields"] = request.form.get("field")
                register_user["actor"] = "doctor"
                register_user["ServiceDate"] = request.form.get("serviceDate")
                register_user["_id"] = "D"+str(hash(register_user["Date_of_Birth"]+str(register_user["Contact"])))[1:7]
            
            collection.insert_one(register_user)

            # put the new user into 'session' cookie
            session["user"] = register_user["_id"]
            session["actor"] = actor
            flash("Registration Successful!", "success")
            return redirect(url_for("profile", user_id=session["user"]))

        return render_template("register.html", actor=actor)
    
    def login(self):
        """
            Find username in db, check that user's password matches what's in
            the db, render login page if no match, render profile page if match.
        """
        actor = request.args.get('actor')
        collection = self.dbClient.db[actor]
        print("We are in login")

        if request.method == "POST":
            # check if username exists in db
            existing_user = collection.find_one(
                {"username": request.form.get("username").lower()})

            if existing_user:
                # ensure hashed password matches user input
                if check_password_hash(
                        existing_user["password"], request.form.get("password")):
                    session["user"] = existing_user["_id"]
                    session["actor"] = actor
                    flash("Welcome, {}".format(
                        request.form.get("username")), "success")
                    return redirect(url_for(
                        "profile", user_id=session["user"]))
                else:
                    # invalid password match
                    flash("Incorrect Username and/or Password", "danger")
                    return redirect(url_for("login"))

            else:
                # username doesn't exist
                flash("Incorrect Username and/or Password", "danger")
                return redirect(url_for("login"))

        return render_template("login.html", actor=actor)
    
    @login_required
    def logout():
        flash("You have been logged out")
        print("We are in logout")
        session.pop("user")
        session.pop("actor")
        return redirect(url_for("home"))
    
    @login_required
    def profile(self, user_id):
        flash("You have been logged out")
        print("We are in profile")
        collection = self.dbClient.db[session["actor"]]
        user = collection.find_one({"_id":user_id})
            
        return render_template(
                "profile.html",
                user_details=user)
    

