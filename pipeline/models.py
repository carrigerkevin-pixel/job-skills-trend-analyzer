import os
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker

# Build an absolute path to the data folder, no matter where this script is run from
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "jobs.db")

engine = create_engine(f"sqlite:///{DB_PATH}")

# Base class that our table classes will inherit from
Base = declarative_base()

class JobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    adzuna_id = Column(String, unique=True, nullable=False)
    title = Column(String)
    company = Column(String)
    location = Column(String)
    description = Column(String)
    date_posted = Column(Date)
    date_collected = Column(Date)
    url = Column(String)

class ExtractedSkill(Base):
    __tablename__ = "extracted_skills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, nullable=False)
    skill_name = Column(String, nullable=False)
    date_extracted = Column(Date)

# This creates the actual database file and table if they don't exist yet
def init_db():
    Base.metadata.create_all(engine)

# This gives us a way to open a "session" to talk to the database
Session = sessionmaker(bind=engine)