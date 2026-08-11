import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker

"""Database models and connection setup for the job skills analyzer.

Defines the SQLAlchemy ORM models for storing job postings, extracted
skills, and historical skill-count snapshots, plus the engine/session
configuration used to connect to the PostgreSQL database.
"""

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found. Make sure it's set in your .env file.")

engine = create_engine(DATABASE_URL)

# Base class that our table classes will inherit from
Base = declarative_base()

class JobPosting(Base):
    """A single job posting collected from the Adzuna API.

    Stores the raw posting details along with which search category
    it was collected under (e.g. "backend developer").
    """
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    adzuna_id = Column(String, unique=True, nullable=False)
    title = Column(String)
    company = Column(String)
    location = Column(String)
    description = Column(String)
    full_description = Column(String)
    date_posted = Column(Date)
    date_collected = Column(Date)
    url = Column(String)
    search_category = Column(String)

class ExtractedSkill(Base):
    """A single skill mention found in a job posting's description.

    One row per (job, skill) pair — a job posting mentioning 5 skills
    will have 5 corresponding rows here, each linked back via job_id.
    """

    __tablename__ = "extracted_skills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, nullable=False)
    skill_name = Column(String, nullable=False)
    date_extracted = Column(Date)

# This creates the actual database file and table if they don't exist yet
def init_db():
    """Create all database tables if they don't already exist.

    Safe to call multiple times — existing tables are left untouched.
    """
    Base.metadata.create_all(engine)

class SkillSnapshot(Base):
    """A historical record of a skill's mention count on a given date.

    Saved periodically (e.g. weekly) to build up trend data over time,
    both overall and broken down by job category.
    """

    __tablename__ = "skill_snapshots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    skill_name = Column(String, nullable=False)
    category = Column(String)  # None/null means "overall", not tied to one category
    count = Column(Integer, nullable=False)
    snapshot_date = Column(Date, nullable=False)

# This gives us a way to open a "session" to talk to the database
Session = sessionmaker(bind=engine)