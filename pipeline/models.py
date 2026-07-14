from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker

# This tells SQLAlchemy where the database file lives
engine = create_engine("sqlite:///data/jobs.db")

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

# This creates the actual database file and table if they don't exist yet
def init_db():
    Base.metadata.create_all(engine)

# This gives us a way to open a "session" to talk to the database
Session = sessionmaker(bind=engine)