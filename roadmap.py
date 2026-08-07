import os
import json

from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    flash
)

roadmap = Blueprint("roadmap", __name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROADMAP_PATH = os.path.join(
    BASE_DIR,
    "model",
    "learning_roadmap.json"
)

with open(ROADMAP_PATH, "r") as file:
    roadmap_data = json.load(file)


@roadmap.route("/roadmap")
def roadmap_page():

    if "user" not in session:
        return redirect("/login")

    if "prediction_result" not in session:

        flash(
            "Please upload your resume first.",
            "warning"
        )

        return redirect("/resume")

    prediction = session.get("prediction_result", {})

    career = str(

        session.get(
            "selected_career",
            prediction.get("career")
        )

    ).strip()

    available_careers = {
    key.strip().lower(): key
    for key in roadmap_data.keys()
}

    career_key = available_careers.get(career.lower())

    if career_key is None:

        flash(
            "Roadmap not available for this career.",
            "warning"
        )

        return redirect("/career")

    return render_template(

    "roadmap.html",

    username=session["user"],

    career=career_key,

    roadmap=roadmap_data[career_key]

)