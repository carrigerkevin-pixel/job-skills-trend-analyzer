from models import Session, JobPosting

session = Session()
jobs = session.query(JobPosting).all()

print(f"Total jobs in database: {len(jobs)}")
for job in jobs[:5]:
    print(f"- {job.title} at {job.company} ({job.location})")

session.close()

from models import ExtractedSkill

skills_count = session.query(ExtractedSkill).count()
print(f"Total extracted skills in database: {skills_count}")

from sqlalchemy import func

print("\nTop skills found:")
results = (
    session.query(ExtractedSkill.skill_name, func.count(ExtractedSkill.id))
    .group_by(ExtractedSkill.skill_name)
    .order_by(func.count(ExtractedSkill.id).desc())
    .all()
)
for skill, count in results:
    print(f"{skill}: {count}")

    sample_job = session.query(JobPosting).first()
print("Description length:", len(sample_job.description))
print(sample_job.description)