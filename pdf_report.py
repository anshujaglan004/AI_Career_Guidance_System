import io

from flask import (
    Blueprint,
    session,
    redirect,
    send_file,
    flash
)

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

pdf_report = Blueprint("pdf_report", __name__)


@pdf_report.route("/download-report")
def download_report():

    if "user" not in session:
        return redirect("/login")

    if "prediction_result" not in session:

        flash(
            "Please upload your resume first.",
            "warning"
        )

        return redirect("/resume")

    report = session["prediction_result"]

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []
    # ==========================================================
    # Title
    # ==========================================================

    story.append(
        Paragraph(
            "<b><font size=18>AI Career Guidance Report</font></b>",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    # ==========================================================
    # User Information
    # ==========================================================

    story.append(
        Paragraph(
            f"<b>User:</b> {session['user']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Resume Score:</b> {report['resume_score']}%",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Recommended Career:</b> {report['career']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Qualification:</b> {report['qualification']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Experience Level:</b> {report['experience']}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 20))

    # ==========================================================
    # Skills Found
    # ==========================================================

    story.append(
        Paragraph(
            "<b>Skills Found</b>",
            styles["Heading2"]
        )
    )

    for skill in report["skills_found"]:

        story.append(
            Paragraph(
                f"• {skill}",
                styles["Normal"]
            )
        )

    story.append(Spacer(1, 20))

    # ==========================================================
    # Missing Skills
    # ==========================================================

    story.append(
        Paragraph(
            "<b>Missing Skills</b>",
            styles["Heading2"]
        )
    )

    if len(report["missing_skills"]) == 0:

        story.append(
            Paragraph(
                "No missing skills detected.",
                styles["Normal"]
            )
        )

    else:

        for skill in report["missing_skills"]:

            story.append(
                Paragraph(
                    f"• {skill}",
                    styles["Normal"]
                )
            )

    story.append(Spacer(1, 20))

    # ==========================================================
    # Suggestions
    # ==========================================================

    story.append(
        Paragraph(
            "<b>Suggestions</b>",
            styles["Heading2"]
        )
    )

    for suggestion in report["suggestions"]:

        story.append(
            Paragraph(
                f"• {suggestion}",
                styles["Normal"]
            )
        )

    story.append(Spacer(1, 20))
    # ==========================================================
    # Footer
    # ==========================================================

    story.append(
        Paragraph(
            "<b>Thank you for using AI Career Guidance System.</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            "Keep learning, improve your skills, and continue building projects to achieve your dream career.",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 20))

    # ==========================================================
    # Generate PDF
    # ==========================================================

    doc.build(story)

    buffer.seek(0)

    return send_file(

        buffer,

        as_attachment=True,

        download_name="AI_Career_Report.pdf",

        mimetype="application/pdf"

    )