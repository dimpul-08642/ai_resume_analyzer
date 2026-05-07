import re
from collections import Counter

# ==============================
# SKILLS DATABASE
# ==============================
SKILLS_DB = [
    "python", "java", "c", "c++", "c#", "javascript",
    "typescript", "html", "css", "react", "angular", "vue",
    "node.js", "node", "express", "django", "flask",
    "sql", "postgresql", "mysql", "mongodb", "redis",
    "rest api", "graphql", "docker", "kubernetes", "aws",
    "azure", "gcp", "linux", "git", "github", "gitlab",
    "ci/cd", "terraform", "ansible", "apache", "nginx",
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
    "keras", "jupyter", "nlp", "computer vision", "machine learning",
    "deep learning", "data science", "data analysis", "analytics",
    "system design", "microservices", "distributed systems",
    "security", "cloud", "unit testing", "api development",
    "restful", "automation", "performance tuning"
]

STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "have",
    "are", "will", "using", "use", "experience", "responsibilities",
    "skills", "required", "preferred", "team", "work", "role",
    "candidate", "job", "knowledge", "years", "year", "strong",
    "ability", "project", "projects", "including", "based", "technical",
    "business", "development", "support", "working", "company"
}


def normalize_text(text):
    return re.sub(r"[^a-z0-9 ]", " ", text.lower())


def extract_skills(text):
    if not text:
        return []

    normalized = normalize_text(text)
    found = set()

    for skill in SKILLS_DB:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, normalized):
            found.add(skill)

    return sorted(found)


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