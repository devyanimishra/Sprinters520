from flask import (session, flash, redirect, url_for)
from functools import wraps

def login_required(f):
    """
        Page is only accessed if user is logged in
        @login_required decorator
        https://flask.palletsprojects.com/en/2.0.x/patterns/viewdecorators/#login-required-decorator
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # no "user" in session
        if "user" not in session:
            flash("You must log in to view this page", "danger")
            return redirect(url_for("login"))
        # user is in session
        return f(*args, **kwargs)
    return decorated_function

def patient_login_required(f):
    """
        Page is only accessed if user is logged in
        @login_required decorator
        https://flask.palletsprojects.com/en/2.0.x/patterns/viewdecorators/#login-required-decorator
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # no "user" in session
        if "user" not in session:
            flash("You must log in to view this page", "danger")
            return redirect(url_for("login"))
        if session["actor"] != "patient":
            flash("You must be a patient log in to view this page", "danger")
            return redirect(url_for("login"))
        # user is in session
        return f(*args, **kwargs)
    return decorated_function

