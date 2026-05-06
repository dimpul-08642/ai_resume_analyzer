import re

# ==============================
# SKILLS DATABASE
# ==============================
SKILLS_DB = [
    "python", "java", "c", "c++", "javascript",
    "html", "css", "react", "node", "express",
    "mongodb", "sql", "mysql",
    "machine learning", "ai", "data science",
    "tensorflow", "pytorch", "pandas", "numpy",
    "git", "github", "docker", "aws",
    "linux", "rest api", "system design"
]

# ==============================
# ✅ IMPROVED SKILL EXTRACTION
# ==============================
def extract_skills(text):
    if not text:
        return []

    text = text.lower()
    found_skills = []

    for skill in SKILLS_DB:
        # Handle multi-word skills properly
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(list(set(found_skills)))


# ==============================
# 🚀 ADVANCED SUGGESTIONS ENGINE
# ==============================
def generate_suggestions(resume_text, resume_skills, job_skills):

    suggestions = []

    resume_text_lower = resume_text.lower()
    resume_set = set(resume_skills)
    job_set = set(job_skills)

    missing = list(job_set - resume_set)

    # ==========================
    # 🎯 1. Missing Skills
    # ==========================
    if missing:
        suggestions.append(
            "Consider adding these key skills to match the job requirements: "
            + ", ".join(missing[:6])
        )

    # ==========================
    # 📌 2. Projects Section
    # ==========================
    if "project" not in resume_text_lower:
        suggestions.append(
            "Include a dedicated 'Projects' section showcasing real-world implementations and technologies used."
        )

    # ==========================
    # 📊 3. Achievements / Metrics
    # ==========================
    if "%" not in resume_text and "improved" not in resume_text_lower:
        suggestions.append(
            "Add measurable achievements (e.g., 'improved performance by 30%') to demonstrate impact."
        )

    # ==========================
    # 🔍 4. Keyword Optimization
    # ==========================
    match_count = len(resume_set & job_set)

    if match_count < 3:
        suggestions.append(
            "Optimize your resume with more relevant keywords from the job description to improve ATS ranking."
        )

    # ==========================
    # 🧠 5. Experience Quality
    # ==========================
    if "experience" not in resume_text_lower:
        suggestions.append(
            "Highlight your experience clearly with roles, responsibilities, and technologies used."
        )

    # ==========================
    # 🧾 6. Resume Structure
    # ==========================
    if len(resume_text.split()) < 150:
        suggestions.append(
            "Your resume seems short. Consider adding more details about projects, skills, and achievements."
        )

    # ==========================
    # ⭐ FINAL FALLBACK
    # ==========================
    if not suggestions:
        suggestions.append(
            "Your resume is well aligned with the job description. Minor optimizations can further improve your profile."
        )

    return suggestions