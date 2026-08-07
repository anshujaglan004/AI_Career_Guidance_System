import os
import json

from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    flash
)

interview = Blueprint("interview", __name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

QUESTION_FILE = os.path.join(
    BASE_DIR,
    "model",
    "interview_questions.json"
)

with open(QUESTION_FILE, "r", encoding="utf-8") as file:
    interview_data = json.load(file)


@interview.route("/interview")
def interview_page():

    # Login Required
    if "user" not in session:
        return redirect("/login")

    # Resume Required
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
    for key in interview_data.keys()
}

    career_key = available_careers.get(career.lower())

    print("=" * 50)
    print("Selected Career:", career)
    print("Available Careers:", interview_data.keys())
    print("=" * 50)

    if career_key is None:

        flash(
            "Interview questions not available for this career.",
            "warning"
        )

        return redirect("/roadmap")

    questions = interview_data[career_key]

    return render_template(

    "interview.html",

    username=session["user"],

    career=career_key,

    questions=questions

)