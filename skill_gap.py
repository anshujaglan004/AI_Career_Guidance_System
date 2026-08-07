from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    flash
)

skill_gap = Blueprint("skill_gap", __name__)


@skill_gap.route("/skill-gap")
def skill_gap_page():

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

    selected_career = session.get(
        "selected_career",
        prediction.get("career")
    )

    current_skills = prediction.get("skills_found", [])

    missing_skills = prediction.get("missing_skills", [])

    total_required = len(current_skills) + len(missing_skills)

    if total_required == 0:
        match_percentage = 0
    else:
        match_percentage = int(
            (len(current_skills) / total_required) * 100
        )

    return render_template(

    "skill_gap.html",

    username=session["user"],

    career=selected_career,

    current_skills=current_skills,

    missing_skills=missing_skills,

    match_percentage=match_percentage,

    suggestions=prediction.get("suggestions", [])

)