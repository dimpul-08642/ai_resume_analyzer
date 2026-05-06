from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_score(resume_text, job_desc):
    try:
        # ✅ handle empty input
        if not resume_text or not job_desc:
            return 0.0

        docs = [resume_text, job_desc]

        vectorizer = TfidfVectorizer(stop_words="english")
        vectors = vectorizer.fit_transform(docs)

        score = cosine_similarity(vectors[0], vectors[1])[0][0]

        return round(score * 100, 2)

    except Exception as e:
        print("Matcher Error:", e)
        return 0.0