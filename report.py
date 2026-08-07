from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    flash
)

report = Blueprint("report", __name__)


# ==========================================================
# Report Page
# ==========================================================

@report.route("/report")
def report_page():

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

    prediction = session["prediction_result"]

    return render_template(

        "report.html",

        username=session["user"],

        filename=session.get("resume_filename"),

        career=prediction.get("career"),

        top_3_careers=prediction.get("top_3_careers", []),

        resume_score=prediction.get("resume_score"),

        qualification=prediction.get("qualification"),

        experience=prediction.get("experience"),

        skills_found=prediction.get("skills_found"),

        missing_skills=prediction.get("missing_skills"),

        suggestions=prediction.get("suggestions")

    )


# ==========================================================
# Select Career From Top 3
# ==========================================================

@report.route("/select-career/<career_name>")
def select_career(career_name):

    # Save selected career in session
    session["selected_career"] = career_name

    return redirect("/career")