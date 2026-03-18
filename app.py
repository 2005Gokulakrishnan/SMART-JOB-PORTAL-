import streamlit as st
import PyPDF2

st.set_page_config(page_title="SmartHire AI", layout="wide")

# -------------------------------
# DOMAIN SKILLS
# -------------------------------
DOMAIN_SKILLS = {
    "software": ["python","java","react","node","django","flask","sql","mongodb","aws","docker","html","css","javascript"],
    "ai": ["machine learning","deep learning","nlp","tensorflow","pytorch"],
    "ece": ["embedded","microcontroller","vlsi","pcb","arduino"],
}

# -------------------------------
# SYNONYMS
# -------------------------------
SYNONYMS = {
    "react": ["reactjs","react.js"],
    "node": ["nodejs","node.js"],
    "machine learning": ["ml"],
    "deep learning": ["neural network"]
}

# -------------------------------
# LEARNING RESOURCES
# -------------------------------
LEARNING_RESOURCES = {
    "python": "https://www.youtube.com/watch?v=_uQrJ0TkZlc",
    "react": "https://www.youtube.com/watch?v=bMknfKXIFA8",
    "docker": "https://www.youtube.com/watch?v=3c-iBn73dDE",
    "aws": "https://www.youtube.com/watch?v=ulprqHHWlng",
    "machine learning": "https://www.youtube.com/watch?v=GwIo3gDZCVQ"
}

# -------------------------------
# JOBS
# -------------------------------
jobs = [
    {"title": "Python Developer", "desc": "python flask sql machine learning"},
    {"title": "Frontend Developer", "desc": "html css javascript react"},
]

# -------------------------------
# PDF FUNCTION
# -------------------------------
def extract_text_from_pdf(uploaded_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    for page in pdf_reader.pages:
        text += page.extract_text() or ""

    return text

# -------------------------------
# LOGIC FUNCTIONS
# -------------------------------
def detect_domain(text):
    text = text.lower()
    scores = {}

    for domain, skills in DOMAIN_SKILLS.items():
        scores[domain] = sum(1 for s in skills if s in text)

    return max(scores, key=scores.get)


def extract_skills(text, skill_list):
    text = text.lower()
    found = []

    for skill in skill_list:
        if skill in text:
            found.append(skill)
        elif skill in SYNONYMS:
            for syn in SYNONYMS[skill]:
                if syn in text:
                    found.append(skill)

    return list(set(found))

# -------------------------------
# SESSION STORAGE
# -------------------------------
if "applications" not in st.session_state:
    st.session_state.applications = []

# -------------------------------
# UI
# -------------------------------
st.title("🧠 SmartHire AI – Advanced Job Portal")

menu = st.sidebar.selectbox("Menu", ["Apply Job", "My Profile"])

# -------------------------------
# APPLY JOB
# -------------------------------
if menu == "Apply Job":

    st.header("Apply for Job")

    name = st.text_input("Name")
    email = st.text_input("Email")

    job_titles = [j["title"] for j in jobs]
    selected_job = st.selectbox("Select Job", job_titles)

    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    resume = ""

    if uploaded_file is not None:
        resume = extract_text_from_pdf(uploaded_file)
        st.success("✅ Resume uploaded and processed")

    if st.button("Analyze & Apply"):

        if name and email and resume:

            job = next(j for j in jobs if j["title"] == selected_job)

            # Domain detection
            domain = detect_domain(job["desc"])
            skill_list = DOMAIN_SKILLS[domain]

            # Skill extraction
            resume_skills = extract_skills(resume, skill_list)
            jd_skills = extract_skills(job["desc"], skill_list)

            matched = [s for s in jd_skills if s in resume_skills]
            missing = [s for s in jd_skills if s not in resume_skills]

            match = round((len(matched) / max(1, len(jd_skills))) * 100, 2)

            status = "✅ Selected" if match >= 70 else "❌ Rejected"

            # Reasons
            reasons = []
            if missing:
                reasons.append("Missing skills: " + ", ".join(missing))
            if match < 70:
                reasons.append(f"Low match score: {match}%")

            # Suggestions
            suggestions = []
            for skill in missing:
                if skill in LEARNING_RESOURCES:
                    suggestions.append((skill, LEARNING_RESOURCES[skill]))

            # Motivation
            if match < 50:
                motivation = "Don't worry! Improve your skills and try again 🚀"
            elif match < 70:
                motivation = "Good progress! You are close 💪"
            else:
                motivation = "Excellent! You are job ready 🚀"

            # Store
            result = {
                "email": email,
                "job": selected_job,
                "match": match,
                "status": status
            }

            st.session_state.applications.append(result)

            # OUTPUT
            st.subheader("📊 Result")
            st.write("Domain:", domain.upper())
            st.write("Match:", match, "%")
            st.write("Status:", status)

            st.subheader("❌ Reasons")
            for r in reasons:
                st.write("-", r)

            st.subheader("📚 Learning Resources")
            for s in suggestions:
                st.markdown(f"🔹 {s[0]} → [Learn Here]({s[1]})")

            st.subheader("💡 Message")
            st.write(motivation)

        else:
            st.warning("Please fill all fields and upload resume")

# -------------------------------
# PROFILE
# -------------------------------
elif menu == "My Profile":

    st.header("My Applications")

    email = st.text_input("Enter your email")

    if st.button("View Applications"):

        user_apps = [a for a in st.session_state.applications if a["email"] == email]

        if user_apps:
            for app in user_apps:
                st.subheader(app["job"])
                st.write("Match:", app["match"])
                st.write("Status:", app["status"])
                st.write("---")
        else:
            st.warning("No applications found")
