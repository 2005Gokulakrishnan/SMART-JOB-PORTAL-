import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="SmartHire AI", layout="wide")

if "applications" not in st.session_state:
    st.session_state.applications = []

jobs = [
    {"id": 1, "title": "Python Developer", "desc": "Python Flask SQL Machine Learning"},
    {"id": 2, "title": "Frontend Developer", "desc": "HTML CSS JavaScript React"},
]

st.title("🧠 SmartHire AI – Job Portal")

menu = st.sidebar.selectbox("Menu", ["Apply Job", "My Profile"])

if menu == "Apply Job":
    st.header("Apply for Job")

    name = st.text_input("Name")
    email = st.text_input("Email")

    job_titles = [job["title"] for job in jobs]
    selected_job = st.selectbox("Select Job", job_titles)

    resume = st.text_area("Paste Resume")

    if st.button("Apply"):
        if name and email and resume:
            job = next(j for j in jobs if j["title"] == selected_job)

            vectorizer = TfidfVectorizer()
            vectors = vectorizer.fit_transform([resume, job["desc"]])
            score = cosine_similarity(vectors[0], vectors[1])[0][0]
            match = round(score * 100, 2)

            resume_words = set(resume.lower().split())
            jd_words = set(job["desc"].lower().split())
            missing = list(jd_words - resume_words)

            status = "✅ Selected" if match >= 70 else "❌ Rejected"

            result = {
                "name": name,
                "email": email,
                "job": selected_job,
                "match": match,
                "status": status,
                "missing": missing[:5]
            }

            st.session_state.applications.append(result)

            st.success("Application Submitted!")

            st.subheader("Result")
            st.write(f"Match: {match}%")
            st.write(f"Status: {status}")
            st.write("Missing Skills:", missing[:5])

        else:
            st.warning("Fill all fields")

elif menu == "My Profile":
    st.header("My Applications")

    email = st.text_input("Enter your email")

    if st.button("View Applications"):
        results = [a for a in st.session_state.applications if a["email"] == email]

        if results:
            for r in results:
                st.subheader(r["job"])
                st.write(f"Match: {r['match']}%")
                st.write(f"Status: {r['status']}")
                st.write("Missing:", r["missing"])
                st.write("---")
        else:
            st.warning("No applications found")
