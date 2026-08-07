from flask import Flask, render_template
import os
from dotenv import load_dotenv

from routes.skill_gap import skill_gap
from routes.roadmap import roadmap
from routes.interview import interview
from routes.pdf_report import pdf_report
from routes.contact import contact

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", "career_guidance_secret_key")

app.config["UPLOAD_FOLDER"] = "uploads"

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

from routes.auth import auth
from routes.dashboard import dashboard
from routes.resume import resume
from routes.report import report
from routes.career import career


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(dashboard)
app.register_blueprint(resume)
app.register_blueprint(report)
app.register_blueprint(career)
app.register_blueprint(skill_gap)
app.register_blueprint(roadmap)
app.register_blueprint(interview)
app.register_blueprint(pdf_report)
app.register_blueprint(contact)


if __name__ == "__main__":
    app.run(debug=True)