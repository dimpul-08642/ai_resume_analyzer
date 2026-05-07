import docx2txt
from pdfminer.high_level import extract_text
import re

SECTION_HEADINGS = [
    "summary",
    "professional summary",
    "about me",
    "experience",
    "work experience",
    "professional experience",
    "education",
    "skills",
    "technical skills",
    "projects",
    "certifications",
    "achievements",
    "awards",
    "contact"
]


def extract_text_from_pdf(file_path):
    try:
        text = extract_text(file_path)
        return text if text else ""
    except Exception as e:
        print("PDF Error:", e)
        return ""

def _normalize_heading(line):
    return re.sub(r"[^a-z0-9 ]", "", line.lower()).strip()


def parse_resume_sections(text):
    if not text:
        return {"text": "", "sections": {}}

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    sections = {}
    current_section = "header"
    sections[current_section] = []

    for line in lines:
        normalized = _normalize_heading(line)
        if normalized in SECTION_HEADINGS:
            current_section = normalized
            sections[current_section] = []
            continue

        sections[current_section].append(line)

    cleaned = {
        section: "\n".join(lines)
        for section, lines in sections.items()
        if lines
    }

    return {"text": text, "sections": cleaned}

def extract_text_from_docx(file_path):
    try:
        text = docx2txt.process(file_path)
        return text if text else ""
    except Exception as e:
        print("DOCX Error:", e)
        return ""