import os
import pandas as pd

from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    flash
)

career = Blueprint("career", __name__)

# ==========================================================
# Load Career Details CSV
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSV_PATH = os.path.join(
    BASE_DIR,
    "model",
    "career_details.csv"
)

career_data = pd.read_csv(CSV_PATH)


@career.route("/career")
def career_page():

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

    # Predicted Career
    #predicted_career = session["prediction_result"]["career"]

    prediction = session.get("prediction_result", {})

    # Use selected career if user clicked "View Details"
    predicted_career = session.get(
        "selected_career",
        prediction.get("career")
    )
    career_data["career"] = career_data["career"].astype(str).str.strip()

    predicted_career = str(predicted_career).strip()

    print("=" * 60)
    print("Selected Career :", predicted_career)
    print("=" * 60)

    result = career_data[
        career_data["career"].str.lower() ==
        predicted_career.lower()
    ]

    
    if result.empty:

        flash(
            "Career details not found.",
            "danger"
        )

        return redirect("/dashboard")

    career_info = result.iloc[0]

    return render_template(

        "career.html",

        username=session["user"],

        career=career_info

    )