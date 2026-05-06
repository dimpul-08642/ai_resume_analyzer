import docx2txt
from pdfminer.high_level import extract_text


def extract_text_from_pdf(file_path):
    try:
        text = extract_text(file_path)
        return text if text else ""
    except Exception as e:
        print("PDF Error:", e)
        return ""


def extract_text_from_docx(file_path):
    try:
        text = docx2txt.process(file_path)
        return text if text else ""
    except Exception as e:
        print("DOCX Error:", e)
        return ""