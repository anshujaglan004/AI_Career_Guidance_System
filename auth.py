from flask import Blueprint, render_template, request, redirect, session

from services.database import register_user, login_user

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]

        user = login_user(email, password)

        if user:

            session["user"] = user["full_name"]

            return redirect("/dashboard")

        return "Invalid Email or Password"

    return render_template("login.html")


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form["full_name"]

        email = request.form["email"]

        password = request.form["password"]

        result = register_user(full_name, email, password)

        if result:

            return redirect("/login")

        return "Registration Failed"

    return render_template("register.html")


@auth.route("/logout")
def logout():

    session.clear()

    return redirect("/login")