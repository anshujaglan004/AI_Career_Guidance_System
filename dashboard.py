from flask import Blueprint, render_template, session, redirect

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard")
def dashboard_page():

    if "user" not in session:
        return redirect("/login")

    prediction = session.get("prediction_result", {})

    return render_template(
        "dashboard.html",
        username=session["user"],
        prediction=prediction
    )