import streamlit as st

st.set_page_config(page_title="SmartHire AI", layout="wide")

# -------------------------------
# DOMAIN SKILLS (from your HTML)
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
# FUNCTIONS
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
# UI
# -------------------------------

st.title("🧠 SmartHire AI – Advanced Analyzer")

menu = st.sidebar.selectbox("Menu", ["Apply Job", "My Profile"])

if "applications" not in st.session_state:
    st.session_state.applications = []

# -------------------------------
# APPLY
# -------------------------------
if menu == "Apply Job":

    name = st.text_input("Name")
    email = st.text_input("Email")

    job_titles = [j["title"] for j in jobs]
    selected_job = st.selectbox("Select Job", job_titles)

    resume = st.text_area("Paste Resume")

    if st.button("Analyze & Apply"):

        job = next(j for j in jobs if j["title"] == selected_job)

        # Detect domain
        domain = detect_domain(job["desc"])
        skill_list = DOMAIN_SKILLS[domain]

        # Extract skills
        resume_skills = extract_skills(resume, skill_list)
        jd_skills = extract_skills(job["desc"], skill_list)

        # Matching
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
            motivation = "Don't worry! Improve skills and try again 🚀"
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

        st.subheader("📚 Learning")
        for s in suggestions:
            st.markdown(f"🔹 {s[0]} → [Learn Here]({s[1]})")

        st.subheader("💡 Message")
        st.write(motivation)

# -------------------------------
# PROFILE
# -------------------------------
elif menu == "My Profile":

    email = st.text_input("Enter email")

    if st.button("View"):
        user_apps = [a for a in st.session_state.applications if a["email"] == email]

        for app in user_apps:
            st.write(app)
