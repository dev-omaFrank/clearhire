"""Seed Clearhire's database with synthetic demo data.

Resets the local database, creates a couple of demo vacancies, and runs each
synthetic resume in data/demo/resumes/ through the REAL scoring pipeline
(the same steps as pages/apply.py), so the demo shows authentic match scores
and rankings rather than hardcoded numbers.

Usage:
    python seed_demo.py
"""
import os
import sys
import types
import shutil

# --- Make the project's packages importable -------------------------------
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)            # for `src.config...`
sys.path.insert(0, os.path.join(ROOT, "src"))  # for `core`, `utils`, `database`

# db_manager imports streamlit (uses st.context.url to build the apply link).
# Stub it so this script can run outside a Streamlit session.
if "streamlit" not in sys.modules:
    st_stub = types.ModuleType("streamlit")
    st_stub.context = types.SimpleNamespace(url="http://localhost:8501")
    sys.modules["streamlit"] = st_stub

from database import db_manager as db
from utils.text_extractor import extract_text
from utils.anonymizer import anonymize_resume
from core.similarity import calculate_similarity, preprocess_for_tfidf
from core.skills import extract_skills_strict, match_skills_strict
from core.experience import extract_years_of_experience, score_experience
from core.explanation import generate_explanation, get_status, combine_scores

DEMO_RESUMES = os.path.join(ROOT, "data", "demo", "resumes")

# --- Demo content ----------------------------------------------------------
VACANCIES = {
    "backend": {
        "job_title": "Backend Engineer",
        "hiring_company": "Clearhire Demo Co.",
        "ai_match_threshold": 40,
        "job_description": (
            "We are hiring a Backend Engineer to design and build scalable web "
            "services. You will work with Python, Django and FastAPI to build "
            "REST API and microservices, backed by PostgreSQL. Experience with "
            "Docker, Kubernetes, AWS and CI/CD is required. Strong unit testing "
            "and integration testing practices and comfort with Git expected."
        ),
    },
    "frontend": {
        "job_title": "Frontend Developer",
        "hiring_company": "Clearhire Demo Co.",
        "ai_match_threshold": 40,
        "job_description": (
            "We are looking for a Frontend Developer to build responsive, "
            "accessible web applications. You will work with JavaScript, "
            "TypeScript, React and Next.js, styling with CSS, Sass and Tailwind. "
            "Strong responsive design and web accessibility skills, REST API "
            "integration, state management with Redux, and Git are expected."
        ),
    },
}

# resume filename -> which vacancy it applies to
APPLICATIONS = [
    ("marcus_bellweather.txt", "Marcus Bellweather", "backend"),
    ("chidalu_okorie.txt",     "Chidalu Okorie",     "backend"),
    ("nmesoma_ononogbo.txt",   "Nmesoma Ononogbo",   "frontend"),
    ("tobechukwu_madu.txt",    "Tobechukwu Madu",    "frontend"),
    ("adaeze_nwachukwu.txt",   "Adaeze Nwachukwu",   "frontend"),
]


def score_resume(resume_text, candidate_name, job_description):
    """Replicates the scoring pipeline in pages/apply.py."""
    resume_text = anonymize_resume(resume_text, candidate_name=candidate_name)
    resume_clean = preprocess_for_tfidf(resume_text)
    job_clean = preprocess_for_tfidf(job_description)

    match_score = calculate_similarity(resume_clean, job_clean)
    job_skills = extract_skills_strict(job_description)
    skills_match = match_skills_strict(resume_clean, job_skills)
    years = extract_years_of_experience(resume_clean)
    exp_score = score_experience(years)

    if skills_match["match_percentage"] <= 7:
        final_score = 0
        ai_recommendation = "No compatible skills found for this vacancy"
    else:
        final_score = combine_scores(
            match_score, skills_match["match_percentage"], exp_score
        )
        ai_recommendation = generate_explanation(
            final_score, skills_match, exp_score, tfidf_score=match_score
        )

    return final_score, ai_recommendation, skills_match


def main():
    # Reset the database so re-seeding is idempotent.
    if os.path.exists(db.DB_PATH):
        os.remove(db.DB_PATH)
    db.init_database()

    # Copy demo resumes into the live resumes folder so the admin can open them.
    live_resumes = os.path.join(ROOT, "data", "resumes")
    os.makedirs(live_resumes, exist_ok=True)

    # Create vacancies.
    vac_ids = {}
    for key, v in VACANCIES.items():
        vid, _ = db.create_vacancy(
            job_title=v["job_title"],
            job_description=v["job_description"],
            hiring_company=v["hiring_company"],
            ai_match_threshold=v["ai_match_threshold"],
        )
        vac_ids[key] = vid
        print(f"Created vacancy: {v['job_title']} (id={vid})")

    print()

    # Score and insert each application.
    for filename, name, vac_key in APPLICATIONS:
        src_path = os.path.join(DEMO_RESUMES, filename)
        if not os.path.exists(src_path):
            print(f"  ! missing demo resume: {filename} - skipping")
            continue

        # Place a copy in the live resumes folder for the admin to view/download.
        dest_path = os.path.join(live_resumes, f"demo_{filename}")
        shutil.copyfile(src_path, dest_path)

        resume_text = extract_text(src_path)
        vac = VACANCIES[vac_key]
        score, recommendation, skills_match = score_resume(
            resume_text, name, vac["job_description"]
        )

        db.create_submission(
            vacancy_id=vac_ids[vac_key],
            candidate_name=name,
            email=f"{name.lower().replace(' ', '.')}@example.com",
            resume_file_path=os.path.join("data", "resumes", f"demo_{filename}"),
            match_score=score,
            ai_recommendation=recommendation,
            strengths=", ".join(skills_match["matched"][:5]),
            gaps=", ".join(skills_match["missing"][:5]),
        )
        print(f"  {name:20s} -> {vac['job_title']:18s}  score: {score:.1f}%")

    print("\nDone. Run the app and open the Admin Dashboard to see the demo data.")


if __name__ == "__main__":
    main()
