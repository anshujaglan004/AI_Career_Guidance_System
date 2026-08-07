import os
import uuid

from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    flash,
    current_app
)

from werkzeug.utils import secure_filename

# Import multi-format text extraction & career prediction services
from services.pdf_service import extract_text_from_file
from services.ml_service import predict_career_from_resume

resume = Blueprint("resume", __name__)

# Allowed file formats
ALLOWED_EXTENSIONS = {"pdf", "txt"}


def allowed_file(filename):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@resume.route("/resume", methods=["GET", "POST"])
def resume_page():

    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":

        if "resume" not in request.files:
            flash("Please select a PDF or TXT file.", "danger")
            return redirect(request.url)

        file = request.files["resume"]

        if file.filename == "":
            flash("No file selected.", "warning")
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash("Only PDF and TXT files are allowed.", "danger")
            return redirect(request.url)

        try:

            # Create upload folder if it doesn't exist
            os.makedirs(
                current_app.config["UPLOAD_FOLDER"],
                exist_ok=True
            )

            filename = secure_filename(file.filename)

            unique_filename = f"{uuid.uuid4().hex}_{filename}"

            filepath = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                unique_filename
            )

            # Save uploaded file
            file.save(filepath)

            # ====================================
            # Extract Resume Text (PDF / TXT)
            # ====================================

            resume_text = extract_text_from_file(filepath)

            if not resume_text or not resume_text.strip():

                flash(
                    "Unable to extract text from the file.",
                    "danger"
                )

                return redirect(request.url)

            # ====================================
            # Predict Career Using ML Model
            # ====================================

            prediction_result = predict_career_from_resume(resume_text)
            print("=" * 60)
            print(prediction_result)
            print("=" * 60)
            # ====================================
            # Save Results in Session
            # ====================================

            session["resume_text"] = resume_text

            session["resume_uploaded"] = True

            session["resume_filename"] = filename

            session["prediction_result"] = prediction_result
            print("Session Career:", session["prediction_result"]["career"])

            return redirect("/report")

        except Exception as e:

            flash(
                f"Error: {str(e)}",
                "danger"
            )

            return redirect(request.url)

    return render_template(
        "resume.html",
        username=session["user"]
    )