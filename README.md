# AI Resume Analyzer

This project is a stronger resume analysis tool that reads PDF/DOCX resumes, extracts skills, parses sections, and generates actionable suggestions to help improve job fit.

## Features

- Resume parsing for PDF and DOCX files
- Expanded skill matching database
- Job keyword extraction from the job description
- Resume structure analysis and section detection
- ATS-style match score and overall resume strength score
- Actionable recommendations for projects, achievements, and keywords
- PDF report download with matched skills, missing skills, and suggestions

## Run locally

```bash
cd backend
python app.py
```

Open `http://127.0.0.1:10000` and upload a resume plus a job description.

## Notes

- The current app uses a stronger analyzer module in `backend/advanced_analyzer.py`
- The new UI is served from `backend/templates/index_new.html`
- For production, use a WSGI server instead of Flask development mode
