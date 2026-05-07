from flask import Flask, request, jsonify, send_file, render_template
import os
import re
import traceback
from werkzeug.utils import secure_filename

from resume_parser import extract_text_from_pdf, extract_text_from_docx, parse_resume_sections
from advanced_analyzer import (
    extract_skills,
    extract_job_keywords,
    generate_suggestions,
    calculate_resume_strength
)
from report_generator import generate_report

app = Flask(__name__, template_folder="templates")

# =========================
# 📁 CONFIG
# =========================
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =========================
# ✅ FILE VALIDATION
# =========================
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# =========================
# 🏠 HOME ROUTE
# =========================
@app.route("/")
def home():
    return render_template("index_new.html")


# =========================
# 🤖 AI FEEDBACK ENGINE
# =========================
def get_ai_feedback(resume_text, job_desc, resume_skills, job_skills):

    resume_set = set(resume_skills)
    job_set = set(job_skills)

    matched = sorted(list(resume_set & job_set))
    missing = sorted(list(job_set - resume_set))

    score = (len(matched) / len(job_set)) * 100 if job_set else 0

    if score >= 80:
        decision = "Strong Match - Recommended"
        summary = "Your profile strongly aligns with the job requirements."
    elif score >= 50:
        decision = "Moderate Match - Consider"
        summary = "Your profile partially matches the job requirements."
    else:
        decision = "Weak Match - Not Recommended"
        summary = "Your profile lacks several key requirements."

    feedback = summary
    if missing:
        feedback += " Focus on adding: " + ", ".join(missing[:6]) + "."

    return {
        "score": round(score, 2),
        "matched_skills": matched,
        "missing_skills": missing,
        "decision": decision,
        "feedback": feedback
    }


# =========================
# 📊 RADAR CHART DATA
# =========================
def generate_skill_chart_data(resume_text, resume_skills, job_skills, job_keywords):
    labels = []
    for item in job_skills + job_keywords + resume_skills:
        if item not in labels:
            labels.append(item)
        if len(labels) >= 10:
            break

    resume_text_lower = resume_text.lower()
    resume_values = [
        1 if skill in resume_skills or re.search(r"\b" + re.escape(skill.lower()) + r"\b", resume_text_lower) else 0
        for skill in labels
    ]
    job_values = [
        1 if skill in job_skills or skill in job_keywords else 0
        for skill in labels
    ]

    return {
        "labels": labels,
        "resume": resume_values,
        "job": job_values
    }


# =========================
# 🚀 ANALYZE ROUTE
# =========================
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        print("📡 Request received")

        file = request.files.get("resume")
        job_desc = request.form.get("job_desc", "").strip()

        # ❌ VALIDATIONS
        if not file:
            return jsonify({"error": "No resume uploaded"}), 400

        if not allowed_file(file.filename):
            return jsonify({"error": "Only PDF/DOCX files allowed"}), 400

        if not job_desc:
            return jsonify({"error": "Job description is required"}), 400

        # ✅ Safe filename
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        # =========================
        # 📄 Extract Resume Text
        # =========================
        if filename.endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        else:
            text = extract_text_from_docx(file_path)

        # =========================
        # 📄 Parse Resume Structure
        # =========================
        resume_data = parse_resume_sections(text)
        resume_sections = resume_data.get("sections", {})

        # =========================
        # 🧠 Extract Skills
        # =========================
        resume_skills = extract_skills(text)
        job_skills = extract_skills(job_desc)
        job_keywords = extract_job_keywords(job_desc)

        # =========================
        # 🤖 Score + Suggestions
        # =========================
        matched = sorted(list(set(resume_skills) & set(job_skills)))
        missing = sorted(list(set(job_skills) - set(resume_skills)))
        strength_score = calculate_resume_strength(text, matched, missing, resume_sections)
        suggestions = generate_suggestions(text, resume_skills, job_skills, resume_sections)

        result = {
            "score": round((len(matched) / len(job_skills) * 100) if job_skills else 0, 2),
            "strength_score": strength_score,
            "matched_skills": matched,
            "missing_skills": missing,
            "job_keywords": job_keywords,
            "sections": resume_sections,
            "suggestions": suggestions,
            "feedback": (
                "Your resume score reflects skill alignment and structure. "
                "Use the recommendations below to add stronger achievements, keywords, and sections."
            )
        }

        result["chart"] = generate_skill_chart_data(text, resume_skills, job_skills, job_keywords)

        return jsonify(result)

    except Exception as e:
        print("❌ ERROR:", traceback.format_exc())
        return jsonify({"error": str(e)}), 500


# =========================
# 📄 REPORT DOWNLOAD
# =========================
@app.route("/download-report", methods=["POST"])
def download_report():
    try:
        data = request.json

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            "AI_Resume_Report.pdf"
        )

        generate_report(file_path, data)

        return send_file(file_path, as_attachment=True, download_name="report.pdf")

    except Exception as e:
        print("❌ REPORT ERROR:", e)
        return jsonify({"error": "Report generation failed"}), 500


# =========================
# ▶️ RUN APP
# =========================
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)