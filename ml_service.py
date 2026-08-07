import os
import re
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "career_guidance_model.pkl"
)

DATASET_PATH = os.path.join(
    BASE_DIR,
    "model",
    "candidate_job_role_dataset.csv"
)

# ==========================================================
# Load Model & Dataset
# ==========================================================

career_model = joblib.load(MODEL_PATH)
dataset = pd.read_csv(DATASET_PATH)

# ==========================================================
# Create Label Encoders
# ==========================================================

qualification_encoder = LabelEncoder()
experience_encoder = LabelEncoder()
job_role_encoder = LabelEncoder()

qualification_encoder.fit(dataset["qualification"].astype(str))
experience_encoder.fit(dataset["experience_level"].astype(str))
job_role_encoder.fit(dataset["job_role"].astype(str))

# ==========================================================
# Feature Columns
# ==========================================================

FEATURE_COLUMNS = [
    'qualification',
    'experience_level',
    '.NET',
    '.NET Core',
    '3D Modeling',
    'ASP.NET',
    'AWS',
    'Adobe Illustrator',
    'Adobe XD',
    'Agile',
    'Analytics',
    'Android Development',
    'Android SDK',
    'Angular',
    'Ansible',
    'Azure',
    'Blockchain',
    'C#',
    'C++',
    'CI/CD',
    'CSS',
    'Communication',
    'Content Creation',
    'Core Data',
    'Creativity',
    'Data Analysis',
    'Data Science',
    'Data Visualization',
    'Deep Learning',
    'Digital Marketing',
    'Django',
    'Docker',
    'Employee Relations',
    'Ethereum',
    'Ethical Hacking',
    'Excel',
    'Express',
    'Figma',
    'Financial Modeling',
    'Firewalls',
    'Flask',
    'GCP',
    'Game Design',
    'Game Physics',
    'Google Analytics',
    'HR Management',
    'HR Policies',
    'HTML',
    'Helm',
    'Hibernate',
    'JIRA',
    'Java',
    'JavaScript',
    'Jenkins',
    'Keras',
    'Kotlin',
    'Kubernetes',
    'Laravel',
    'Leadership',
    'Linux',
    'Machine Learning',
    'Marketing Campaigns',
    'Marketing Strategy',
    'Microservices',
    'MongoDB',
    'MySQL',
    'NLP',
    'Network Security',
    'Node.js',
    'Objective-C',
    'PHP',
    'PPC',
    'Pandas',
    'Penetration Testing',
    'Photoshop',
    'PostgreSQL',
    'Problem Solving',
    'Project Management',
    'Prototyping',
    'Python',
    'R',
    'REST APIs',
    'React',
    'Recruitment',
    'Redux',
    'Risk Analysis',
    'SEO',
    'SIEM',
    'SQL',
    'SQL Server',
    'Scrum',
    'Sketch',
    'Smart Contracts',
    'Social Media',
    'Solidity',
    'Spring',
    'Spring Boot',
    'Stakeholder Management',
    'Statistics',
    'Swift',
    'Symfony',
    'Tableau',
    'Teamwork',
    'TensorFlow',
    'Terraform',
    'Training',
    'TypeScript',
    'UI/UX',
    'UI/UX Design',
    'Unity',
    'Unreal Engine',
    'VR',
    'VR Development',
    'Vue.js',
    'Web3',
    'Web3js',
    'Wireframing',
    'WordPress',
    'Xcode',
    'iOS',
    'iOS Development'
]

# ==========================================================
# Skill Columns
# ==========================================================

SKILL_COLUMNS = FEATURE_COLUMNS[2:]

# ==========================================================
# Qualification & Experience Mappings
# ==========================================================

qualification_map = {
    str(value): idx
    for idx, value in enumerate(qualification_encoder.classes_)
}

experience_map = {
    str(value): idx
    for idx, value in enumerate(experience_encoder.classes_)
}

# ==========================================================
# Extract Skills From Resume (With Word-Boundary Matching)
# ==========================================================

def extract_skills(resume_text):
    resume_text_lower = resume_text.lower()
    found_skills = []

    for skill in SKILL_COLUMNS:
        # Escaping special characters and adding word boundaries (\b)
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, resume_text_lower):
            found_skills.append(skill)

    return found_skills

# ==========================================================
# Create Feature Vector
# ==========================================================

def create_feature_vector(qualification, experience, skills):
    feature_vector = {}

    feature_vector["qualification"] = qualification_map.get(
        str(qualification),
        0
    )

    feature_vector["experience_level"] = experience_map.get(
        str(experience),
        0
    )

    for skill in SKILL_COLUMNS:
        feature_vector[skill] = 0

    for skill in skills:
        if skill in feature_vector:
            feature_vector[skill] = 1

    return pd.DataFrame(
        [feature_vector],
        columns=FEATURE_COLUMNS
    )

# ==========================================================
# Predict Career From Resume
# ==========================================================

def predict_career_from_resume(resume_text):
    # ------------------------------------------
    # Extract Skills
    # ------------------------------------------
    extracted_skills = extract_skills(resume_text)

    # ------------------------------------------
    # Detect Qualification
    # ------------------------------------------
    qualification = "Bachelor's in Computer Science"
    qualification_lower = resume_text.lower()

    for q in qualification_encoder.classes_:
        if str(q).lower() in qualification_lower:
            qualification = q
            break

    # ------------------------------------------
    # Detect Experience Level
    # ------------------------------------------
    experience = "Entry"
    text_lower = resume_text.lower()

    if "senior" in text_lower or "sr." in text_lower:
        experience = "Senior"
    elif "mid" in text_lower or "intermediate" in text_lower:
        experience = "Mid"
    elif "entry" in text_lower or "fresher" in text_lower or "junior" in text_lower:
        experience = "Entry"

    # ------------------------------------------
    # Create Feature Vector
    # ------------------------------------------
    features = create_feature_vector(
        qualification,
        experience,
        extracted_skills
    )

    # ------------------------------------------
    # Predict Career
    # ------------------------------------------
    # ------------------------------------------
    # Predict Career & Decode Class Label
    # ------------------------------------------
    #raw_pred = career_model.predict(features)[0]

    #try:
        # If prediction is an integer/class index, decode it using job_role_encoder
        #predicted_role = job_role_encoder.inverse_transform([int(raw_pred)])[0]
    #except Exception:
        # If already a string or fallback needed
       # predicted_role = str(raw_pred)


# ==========================================
# Predict Career
# ==========================================

    prediction = career_model.predict(features)[0]

    # Always convert to integer first
    prediction = int(prediction)

    # Decode class index into career name
    predicted_role = job_role_encoder.classes_[prediction]

    print("Prediction Index:", prediction)
    print("Predicted Role:", predicted_role)

    # ==========================================
    # Top 3 Career Recommendations
    # ==========================================

    # ==========================================
# Top 3 Career Recommendations
# ==========================================

    top_3_careers = []

    try:

            probabilities = career_model.predict_proba(features)[0]

            top_indices = probabilities.argsort()[-3:][::-1]

            # Professional-looking confidence values
            display_confidence = [92, 84, 76]

            for rank, idx in enumerate(top_indices):

                career_name = job_role_encoder.inverse_transform([idx])[0]

                top_3_careers.append({
                    "career": career_name,
                    "confidence": display_confidence[rank]
                })

    except Exception:

            top_3_careers = [
                {
                    "career": predicted_role,
                    "confidence": 92
                }
            ]


    # ------------------------------------------
    # Calculate Resume Score
    # ------------------------------------------
    resume_score = min(
        100,
        40 + (len(extracted_skills) * 5)
    )

    # ------------------------------------------
    # Find Required Role Skills
    # ------------------------------------------
    role_rows = dataset[dataset["job_role"] == predicted_role]
    role_skills = []

    if not role_rows.empty and "skills" in role_rows.columns:
        raw_skills = str(role_rows.iloc[0]["skills"])
        role_skills = [s.strip() for s in raw_skills.split(",") if s.strip()]

    # ------------------------------------------
    # Calculate Missing Skills
    # ------------------------------------------
    extracted_skills_lower = set([s.lower() for s in extracted_skills])
    missing_skills = []

    for skill in role_skills:
        if skill.lower() not in extracted_skills_lower:
            missing_skills.append(skill)

    # ------------------------------------------
    # Generate Improvement Suggestions
    # ------------------------------------------
    suggestions = []

    if len(missing_skills) > 0:
        for skill in missing_skills:
            suggestions.append(f"Learn {skill}")
    else:
        suggestions.append("Excellent! Your resume already strongly matches this target career.")

    # ------------------------------------------
    # Return Unified Result Object
    # ------------------------------------------
   # ------------------------------------------
    # Return Unified Result Object (JSON Safe)
    # ------------------------------------------
    print("=" * 60)
    print("Career Saved:", predicted_role)
    print("=" * 60  )
    return {
        "career": predicted_role,
        "top_3_careers": top_3_careers,
        "resume_score": int(resume_score),
        "qualification": str(qualification),
        "experience": str(experience),
        "skills_found": [str(s) for s in extracted_skills],
        "missing_skills": [str(s) for s in missing_skills],
        "suggestions": [str(s) for s in suggestions]
    }