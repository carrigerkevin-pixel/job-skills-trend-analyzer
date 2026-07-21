from datetime import date
from models import Session, JobPosting, ExtractedSkill
from extract_skills import extract_skills_from_text


def run_extraction():
    session = Session()

    jobs = session.query(JobPosting).all()
    print(f"Found {len(jobs)} job postings to process")

    total_skills_saved = 0

    for job in jobs:
        # Check if we've already extracted skills for this job — avoid duplicate work
        already_done = session.query(ExtractedSkill).filter_by(job_id=job.id).first()
        if already_done:
            continue

        skills_found = extract_skills_from_text(job.description)

        for skill in skills_found:
            entry = ExtractedSkill(
                job_id=job.id,
                skill_name=skill,
                date_extracted=date.today()
            )
            session.add(entry)
            total_skills_saved += 1

    session.commit()
    session.close()

    print(f"Saved {total_skills_saved} skill mentions across all jobs")


if __name__ == "__main__":
    run_extraction()