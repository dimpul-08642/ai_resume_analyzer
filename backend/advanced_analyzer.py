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


def extract_job_keywords(text, top_n=8):
    if not text:
        return []

    normalized = normalize_text(text)
    found_skills = extract_skills(text)
    words = re.findall(r"\b[a-z]{3,}\b", normalized)
    filtered = [w for w in words if w not in STOPWORDS]
    counts = Counter(filtered)
    candidates = [word for word, _ in counts.most_common(top_n * 2)]

    keywords = []
    for skill in found_skills:
        if skill not in keywords:
            keywords.append(skill)

    for word in candidates:
        if word not in keywords and len(keywords) < top_n:
            keywords.append(word)

    return keywords


def calculate_resume_strength(resume_text, matched, missing, sections):
    score = 45
    section_names = set(sections.keys())

    score += 10 if "summary" in section_names else 0
    score += 10 if "experience" in section_names or "work experience" in section_names else 0
    score += 8 if "education" in section_names else 0
    score += 6 if "skills" in section_names or "technical skills" in section_names else 0
    score += 6 if "projects" in section_names else 0
    score += 5 if "achievements" in section_names else 0

    score += min(len(matched) * 6, 30)
    score -= min(len(missing) * 4, 20)
    score += 8 if len(resume_text.split()) > 220 else 0

    return round(max(0, min(100, score)), 2)


def generate_suggestions(resume_text, resume_skills, job_skills, sections):
    suggestions = []
    resume_text_lower = resume_text.lower()
    resume_set = set(resume_skills)
    job_set = set(job_skills)
    missing = sorted(list(job_set - resume_set))

    if missing:
        suggestions.append(
            "Add these job-specific skills: " + ", ".join(missing[:8]) + "."
        )

    if "summary" not in sections:
        suggestions.append(
            "Add a concise professional summary at the top to highlight your experience and impact."
        )

    if "experience" not in sections and "work experience" not in sections:
        suggestions.append(
            "Add an Experience section with role titles, company names, dates, and measurable outcomes."
        )

    if "education" not in sections:
        suggestions.append(
            "Include an Education section that lists your degree, institution, and graduation details."
        )

    if "projects" not in sections:
        suggestions.append(
            "Include a Projects section describing strong engineering or analytics work."
        )

    if "%" not in resume_text_lower and "improved" not in resume_text_lower and "achieved" not in resume_text_lower:
        suggestions.append(
            "Use measurable achievements and metrics to show impact (for example, improved performance by 30%)."
        )

    if len(resume_text.split()) < 180:
        suggestions.append(
            "Your resume appears short; add more detail about accomplishments, tools used, and results."
        )

    if len(resume_skills) < len(job_skills) and job_skills:
        suggestions.append(
            "Match your resume keywords more closely with the job description for better ATS performance."
        )

    if not suggestions:
        suggestions.append(
            "Your resume has a solid foundation. Add more metrics and stronger project descriptions for an even better fit."
        )

    return suggestions
