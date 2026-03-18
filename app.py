from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Temporary storage (acts like DB for now)
jobs = [
    {
        "id": 1,
        "title": "Python Developer",
        "description": "Looking for Python, Flask, SQL, and Machine Learning skills"
    },
    {
        "id": 2,
        "title": "Frontend Developer",
        "description": "Looking for HTML, CSS, JavaScript, React"
    }
]

applications = []


@app.route("/")
def home():
    return "SmartHire AI Backend Running 🚀"


# 📌 Get all jobs
@app.route("/jobs", methods=["GET"])
def get_jobs():
    return jsonify(jobs)


# 📌 Apply for job (CORE FEATURE)
@app.route("/apply", methods=["POST"])
def apply():
    data = request.json

    name = data.get("name")
    email = data.get("email")
    resume = data.get("resume")
    job_id = data.get("job_id")

    if not all([name, email, resume, job_id]):
        return jsonify({"error": "Missing fields"}), 400

    # find job
    job = next((j for j in jobs if j["id"] == job_id), None)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    jd = job["description"]

    # 🔥 AI Matching
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume, jd])
    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
    match = round(similarity * 100, 2)

    # missing skills
    resume_words = set(resume.lower().split())
    jd_words = set(jd.lower().split())
    missing = list(jd_words - resume_words)

    status = "Selected" if match >= 70 else "Rejected"

    # store result
    application = {
        "name": name,
        "email": email,
        "job_id": job_id,
        "job_title": job["title"],
        "match": match,
        "status": status,
        "missing_skills": missing[:10]
    }

    applications.append(application)

    return jsonify(application)


# 📌 Profile page (view applications)
@app.route("/my-applications", methods=["GET"])
def my_applications():
    email = request.args.get("email")

    user_apps = [a for a in applications if a["email"] == email]

    return jsonify(user_apps)


if __name__ == "__main__":
    app.run()
