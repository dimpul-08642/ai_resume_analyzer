from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


# =========================
# ✅ SMART CLEAN SKILLS
# =========================
def clean_skills(skills):
    if not skills:
        return []

    # Case 1: already list → good
    if isinstance(skills, list):
        return sorted(set(skills))

    # Case 2: string → FIX HERE
    if isinstance(skills, str):

        # If commas exist → split by comma
        if "," in skills:
            skills = [s.strip() for s in skills.split(",")]

        # Else → assume space-separated words (fallback)
        else:
            words = skills.split()

            # Try grouping known phrases
            grouped = []
            i = 0
            while i < len(words):
                if i < len(words) - 1:
                    pair = words[i] + " " + words[i + 1]

                    if pair in [
                        "machine learning",
                        "data science",
                        "deep learning",
                        "computer vision"
                    ]:
                        grouped.append(pair)
                        i += 2
                        continue

                grouped.append(words[i])
                i += 1

            skills = grouped

    return sorted(set(skills))


# =========================
# 🎯 FORMAT TEXT
# =========================
def format_skills_text(skills):
    skills = clean_skills(skills)

    if not skills:
        return "None"

    return ", ".join(skills)


# =========================
# 🤖 BETTER FEEDBACK
# =========================
def generate_feedback(score, missing):

    if score >= 80:
        text = "The candidate demonstrates a strong alignment with the job requirements. "
    elif score >= 50:
        text = "The candidate shows partial alignment with the job requirements. "
    else:
        text = "The candidate currently lacks several key skills required for this role. "

    if missing:
        text += "Focus on improving these areas: " + ", ".join(missing[:6]) + ". "

    text += (
        "To improve your chances, include relevant projects, highlight measurable achievements, "
        "and tailor your resume using job-specific keywords."
    )

    return text


# =========================
# 📄 MAIN REPORT
# =========================
def generate_report(file_path, data):

    try:
        doc = SimpleDocTemplate(file_path)
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            name="Title",
            fontSize=20,
            alignment=1,
            textColor=colors.darkblue,
            spaceAfter=20
        )

        heading = ParagraphStyle(
            name="Heading",
            fontSize=13,
            textColor=colors.blue,
            spaceAfter=6
        )

        normal = ParagraphStyle(
            name="Normal",
            fontSize=11,
            spaceAfter=10
        )

        content = []

        # TITLE
        content.append(Paragraph("AI Resume Analysis Report", title_style))

        # SCORE
        score = float(data.get("score", 0))
        content.append(Paragraph(f"<b>ATS Score:</b> {score}%", heading))

        # MATCHED SKILLS
        matched = data.get("matched_skills", [])
        matched_text = format_skills_text(matched)

        content.append(Paragraph("<b>Matched Skills</b>", heading))
        content.append(Paragraph("✔ " + matched_text, normal))

        # MISSING SKILLS
        missing = data.get("missing_skills", [])
        missing_text = format_skills_text(missing)

        content.append(Paragraph("<b>Missing Skills</b>", heading))
        content.append(Paragraph("✖ " + missing_text, normal))

        # FEEDBACK
        feedback = generate_feedback(score, clean_skills(missing))

        content.append(Paragraph("<b>AI Feedback</b>", heading))
        content.append(Paragraph(feedback, normal))

        doc.build(content)

        return file_path

    except Exception as e:
        print("ERROR:", e)
        return None