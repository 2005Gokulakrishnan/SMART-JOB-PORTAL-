import streamlit as st
import PyPDF2

st.set_page_config(page_title="SmartHire AI", layout="wide")

# -------------------------------
# BIG SKILL DATABASE
# -------------------------------
SKILLS = [
    "python","java","react","node","django","flask","sql","mongodb","aws","docker",
    "html","css","javascript","machine learning","deep learning","nlp","tensorflow",
    "pytorch","git","linux","kubernetes","c++","data analysis"
]

# -------------------------------
# LEARNING RESOURCES (STRONG)
# -------------------------------
LEARNING_RESOURCES = {
    "python": "https://youtu.be/_uQrJ0TkZlc",
    "react": "https://youtu.be/bMknfKXIFA8",
    "docker": "https://youtu.be/3c-iBn73dDE",
    "aws": "https://youtu.be/ulprqHHWlng",
    "machine learning": "https://youtu.be/GwIo3gDZCVQ",
    "javascript": "https://youtu.be/PkZNo7MFNFg",
    "sql": "https://youtu.be/HXV3zeQKqGY"
}

# -------------------------------
# REALISTIC JOBS
# -------------------------------
jobs = [
    {"title": "Python Backend Developer", "desc": "python flask sql docker aws"},
    {"title": "Frontend Developer", "desc": "html css javascript react"},
    {"title": "Full Stack Developer", "desc": "python react sql docker"},
    {"title": "Machine Learning Engineer", "desc": "python machine learning tensorflow"},
    {"title": "DevOps Engineer", "desc": "docker aws kubernetes linux"}
]

# -------------------------------
# PDF FUNCTION
# -------------------------------
def extract_text_from_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.lower()

# -------------------------------
# SESSION
# -------------------------------
if "applications" not in st.session_state:
    st.session_state.applications = []

# -------------------------------
# UI HEADER
# -------------------------------
st.title("🧠 SmartHire AI")
st.caption("AI-powered Job Matching with Feedback & Growth Suggestions")

menu = st.sidebar.selectbox("Menu", ["Apply Job", "My Profile"])

# -------------------------------
# APPLY PAGE
# -------------------------------
if menu == "Apply Job":

    st.subheader("🚀 Apply for Jobs")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Name")
        email = st.text_input("Email")

    with col2:
        job_titles = [j["title"] for j in jobs]
        selected_job = st.selectbox("Select Job Role", job_titles)

    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    resume = ""
    if uploaded_file:
        resume = extract_text_from_pdf(uploaded_file)
        st.success("Resume processed successfully ✅")

    if st.button("Analyze Application"):

        if not (name and email and resume):
            st.warning("Please complete all fields")
        else:
            job = next(j for j in jobs if j["title"] == selected_job)
            jd = job["desc"]

            # Skill extraction
            resume_skills = [s for s in SKILLS if s in resume]
            jd_skills = [s for s in SKILLS if s in jd]

            matched = [s for s in jd_skills if s in resume_skills]
            missing = [s for s in jd_skills if s not in resume_skills]

            match = round((len(matched) / max(1, len(jd_skills))) * 100, 2)
            status = "✅ Selected" if match >= 70 else "❌ Rejected"

            # -------------------------------
            # BETTER MESSAGES
            # -------------------------------
            if match < 50:
                message = "You're not far away! Focus on key missing skills and try again. Growth takes time 🚀"
            elif match < 70:
                message = "Good progress! You're close to being job-ready. Improve a few areas 💪"
            else:
                message = "Excellent! You are a strong match. Keep pushing forward 🚀"

            # Suggestions
            suggestions = []
            for skill in missing:
                if skill in LEARNING_RESOURCES:
                    suggestions.append((skill, LEARNING_RESOURCES[skill]))

            # Save
            st.session_state.applications.append({
                "email": email,
                "job": selected_job,
                "match": match,
                "status": status
            })

            # -------------------------------
            # OUTPUT UI (CARD STYLE)
            # -------------------------------
            st.markdown("---")
            st.subheader("📊 Analysis Result")

            col1, col2, col3 = st.columns(3)

            col1.metric("Match %", match)
            col2.metric("Status", status)
            col3.metric("Missing Skills", len(missing))

            st.markdown("### ❌ Skill Gap")
            st.write(", ".join(missing) if missing else "No gaps 🎉")

            st.markdown("### 📚 Learning Suggestions")
            if suggestions:
                for s in suggestions:
                    st.markdown(f"🔹 {s[0]} → [Learn Here]({s[1]})")
            else:
                st.write("You're already strong in required skills!")

            st.markdown("### 💡 Message for You")
            st.success(message)

# -------------------------------
# PROFILE
# -------------------------------
elif menu == "My Profile":

    st.subheader("📂 My Applications")

    email = st.text_input("Enter your email")

    if st.button("View"):
        data = [a for a in st.session_state.applications if a["email"] == email]

        if data:
            for d in data:
                st.markdown(f"""
                **Job:** {d['job']}  
                **Match:** {d['match']}%  
                **Status:** {d['status']}  
                ---
                """)
        else:
            st.warning("No applications found")
