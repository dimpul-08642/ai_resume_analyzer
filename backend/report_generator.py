from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


# =========================
# ✅ CLEAN SKILLS
# =========================
def clean_skills(skills):
    if not skills:
        return []

    if isinstance(skills, list):
        return sorted(set(skills))

    if isinstance(skills, str):
        if "," in skills:
            skills = [s.strip() for s in skills.split(",")]
        else:
            skills = [skill.strip() for skill in skills.split() if skill.strip()]

    return sorted(set(skills))


# =========================
# 📄 FORMAT HELPERS
# =========================
def format_skills_text(skills):
    cleaned = clean_skills(skills)
    return ", ".join(cleaned) if cleaned else "None"


def format_section_list(sections):
    if not sections:
        return "None"
    return ", ".join(sorted(sections.keys()))


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
            spaceAfter=8
        )

        content = []
        content.append(Paragraph("AI Resume Analysis Report", title_style))

        score = float(data.get("score", 0))
        content.append(Paragraph(f"<b>ATS Score:</b> {score}%", heading))

        strength = data.get("strength_score")
        if strength is not None:
            content.append(Paragraph(f"<b>Resume Strength:</b> {strength}%", heading))

        content.append(Paragraph("<b>Matched Skills</b>", heading))
        content.append(Paragraph("✔ " + format_skills_text(data.get("matched_skills", [])), normal))

        content.append(Paragraph("<b>Missing Skills</b>", heading))
        content.append(Paragraph("✖ " + format_skills_text(data.get("missing_skills", [])), normal))

        content.append(Paragraph("<b>Job Keywords</b>", heading))
        content.append(Paragraph(format_skills_text(data.get("job_keywords", [])), normal))

        content.append(Paragraph("<b>Sections Detected</b>", heading))
        content.append(Paragraph(format_section_list(data.get("sections", {})), normal))

        suggestions = data.get("suggestions", [])
        if suggestions:
            content.append(Paragraph("<b>Recommendations</b>", heading))
            for suggestion in suggestions:
                content.append(Paragraph("• " + suggestion, normal))

        feedback = data.get("feedback")
        if feedback:
            content.append(Paragraph("<b>AI Feedback</b>", heading))
            content.append(Paragraph(feedback, normal))

        doc.build(content)
        return file_path

    except Exception as e:
        print("ERROR:", e)
        return None