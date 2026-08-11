"""Analysis functions for summarizing skill trends from collected data.

Provides reusable query functions — used by both the FastAPI backend
and the Streamlit dashboard — for computing top skills overall, top
skills by job category, and saving historical snapshots for future
trend-over-time analysis.
"""

from sqlalchemy import func
from models import Session, ExtractedSkill, JobPosting
from datetime import date
from models import SkillSnapshot


def top_skills_overall(limit=10):
    """Get the most frequently mentioned skills across all job postings.

    Args:
        limit (int): Maximum number of skills to return.

    Returns:
        list[dict]: Each item has "skill" (str) and "count" (int) keys,
            ordered from most to least frequent.
    """
     
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
    """Get the most frequently mentioned skills for a specific job category.

    Args:
        category (str): The search category to filter by (e.g.
            "backend developer"), matching JobPosting.search_category.
        limit (int): Maximum number of skills to return.

    Returns:
        list[dict]: Each item has "skill" (str) and "count" (int) keys,
            ordered from most to least frequent within that category.
    """
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
    """Get the list of distinct job search categories in the database.

    Returns:
        list[str]: Unique category names (e.g. "data analyst",
            "frontend developer"), excluding any null values.
    """
    session = Session()
    results = session.query(JobPosting.search_category).distinct().all()
    session.close()
    return [r[0] for r in results if r[0] is not None]

def save_snapshot():
    """Save today's skill counts (overall and per-category) as a permanent snapshot.

    Records a SkillSnapshot row for every skill in the overall ranking
    and every skill in each category's ranking, timestamped with
    today's date. Intended to be run periodically (e.g. weekly via
    the GitHub Actions pipeline) to build up historical trend data.
    """
    session = Session()
    today = date.today()

    # Save overall counts
    for row in top_skills_overall(limit=1000):
        session.add(SkillSnapshot(
            skill_name=row["skill"],
            category=None,
            count=row["count"],
            snapshot_date=today
        ))

    # Save per-category counts
    for category in all_categories():
        for row in top_skills_by_category(category, limit=1000):
            session.add(SkillSnapshot(
                skill_name=row["skill"],
                category=category,
                count=row["count"],
                snapshot_date=today
            ))

    session.commit()
    session.close()
    print(f"Saved snapshot for {today}")


if __name__ == "__main__":
    print("=== Top skills overall ===")
    for row in top_skills_overall():
        print(f"{row['skill']}: {row['count']}")

    print("\n=== Skills by category ===")
    for category in all_categories():
        print(f"\n-- {category} --")
        for row in top_skills_by_category(category, limit=5):
            print(f"{row['skill']}: {row['count']}")

    print("\n=== Saving snapshot ===")
    save_snapshot()