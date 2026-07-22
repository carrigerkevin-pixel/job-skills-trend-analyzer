from sqlalchemy import func
from models import Session, ExtractedSkill, JobPosting


def top_skills_overall(limit=10):
    """Return the most frequently mentioned skills across all jobs."""
    session = Session()

    results = (
        session.query(ExtractedSkill.skill_name, func.count(ExtractedSkill.id))
        .group_by(ExtractedSkill.skill_name)
        .order_by(func.count(ExtractedSkill.id).desc())
        .limit(limit)
        .all()
    )

    session.close()
    return [{"skill": skill, "count": count} for skill, count in results]


def top_skills_by_category(category, limit=10):
    """Return the most frequently mentioned skills for a specific job category."""
    session = Session()

    results = (
        session.query(ExtractedSkill.skill_name, func.count(ExtractedSkill.id))
        .join(JobPosting, ExtractedSkill.job_id == JobPosting.id)
        .filter(JobPosting.search_category == category)
        .group_by(ExtractedSkill.skill_name)
        .order_by(func.count(ExtractedSkill.id).desc())
        .limit(limit)
        .all()
    )

    session.close()
    return [{"skill": skill, "count": count} for skill, count in results]


def all_categories():
    """Return the list of distinct search categories in the database."""
    session = Session()
    results = session.query(JobPosting.search_category).distinct().all()
    session.close()
    return [r[0] for r in results if r[0] is not None]


if __name__ == "__main__":
    print("=== Top skills overall ===")
    for row in top_skills_overall():
        print(f"{row['skill']}: {row['count']}")

    print("\n=== Skills by category ===")
    for category in all_categories():
        print(f"\n-- {category} --")
        for row in top_skills_by_category(category, limit=5):
            print(f"{row['skill']}: {row['count']}")