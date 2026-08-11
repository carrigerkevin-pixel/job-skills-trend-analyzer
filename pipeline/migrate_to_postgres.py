import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, JobPosting, ExtractedSkill, SkillSnapshot, engine as postgres_engine

# Connect to the OLD local SQLite database directly
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQLITE_PATH = os.path.join(BASE_DIR, "data", "jobs.db")
sqlite_engine = create_engine(f"sqlite:///{SQLITE_PATH}")

SqliteSession = sessionmaker(bind=sqlite_engine)
PostgresSession = sessionmaker(bind=postgres_engine)


def migrate():
    sqlite_session = SqliteSession()
    postgres_session = PostgresSession()

    # Migrate job postings
    jobs = sqlite_session.query(JobPosting).all()
    print(f"Migrating {len(jobs)} job postings...")
    for job in jobs:
        new_job = JobPosting(
            id=job.id,
            adzuna_id=job.adzuna_id,
            title=job.title,
            company=job.company,
            location=job.location,
            description=job.description,
            date_posted=job.date_posted,
            date_collected=job.date_collected,
            url=job.url,
            search_category=job.search_category
        )
        postgres_session.merge(new_job)

    # Migrate extracted skills
    skills = sqlite_session.query(ExtractedSkill).all()
    print(f"Migrating {len(skills)} extracted skills...")
    for skill in skills:
        new_skill = ExtractedSkill(
            id=skill.id,
            job_id=skill.job_id,
            skill_name=skill.skill_name,
            date_extracted=skill.date_extracted
        )
        postgres_session.merge(new_skill)

    # Migrate skill snapshots
    snapshots = sqlite_session.query(SkillSnapshot).all()
    print(f"Migrating {len(snapshots)} skill snapshots...")
    for snapshot in snapshots:
        new_snapshot = SkillSnapshot(
            id=snapshot.id,
            skill_name=snapshot.skill_name,
            category=snapshot.category,
            count=snapshot.count,
            snapshot_date=snapshot.snapshot_date
        )
        postgres_session.merge(new_snapshot)

    postgres_session.commit()
    sqlite_session.close()
    postgres_session.close()
    print("Migration complete.")


if __name__ == "__main__":
    migrate()