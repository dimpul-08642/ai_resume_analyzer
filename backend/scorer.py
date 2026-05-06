def calculate_ats(resume_skills, job_skills):

    try:
        # ✅ handle empty input
        if not resume_skills or not job_skills:
            return 0.0

        # ✅ normalize case
        resume_set = set([skill.lower() for skill in resume_skills])
        job_set = set([skill.lower() for skill in job_skills])

        matched = resume_set.intersection(job_set)

        score = (len(matched) / len(job_set)) * 100

        return round(score, 2)

    except Exception as e:
        print("Scorer Error:", e)
        return 0.0