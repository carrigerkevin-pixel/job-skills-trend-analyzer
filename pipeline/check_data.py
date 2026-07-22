from models import Session, JobPosting
from models import SkillSnapshot

session = Session()
jobs = session.query(JobPosting).all()
total = session.query(JobPosting).count()
print(f"Total jobs: {total}")

sample = session.query(JobPosting).first()
print(f"Sample search_category: {sample.search_category}")

# Count jobs per category
from sqlalchemy import func
category_counts = (
    session.query(JobPosting.search_category, func.count(JobPosting.id))
    .group_by(JobPosting.search_category)
    .all()
)
for category, count in category_counts:
    print(f"{category}: {count}")

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

snapshot_count = session.query(SkillSnapshot).count()
print(f"Total snapshot rows: {snapshot_count}")