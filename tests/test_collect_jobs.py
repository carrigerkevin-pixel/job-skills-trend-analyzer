import sys
import os

# Let this test file import from the pipeline folder
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "pipeline"))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, JobPosting
from collect_jobs import save_jobs
from datetime import date


@pytest.fixture
def test_session():
    """Creates a fresh, temporary in-memory database for each test."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_save_new_job(monkeypatch, test_session):
    """A brand new job should be saved to the database."""

    # Replace the real Session with our test session for this test only
    monkeypatch.setattr("collect_jobs.Session", lambda: test_session)

    fake_job = [{
        "id": "12345",
        "title": "Test Engineer",
        "company": {"display_name": "Test Corp"},
        "location": {"display_name": "Remote"},
        "description": "A fake job for testing",
        "created": "2026-07-14T08:00:00Z",
        "redirect_url": "https://example.com/job/12345"
    }]

    save_jobs(fake_job)

    saved = test_session.query(JobPosting).filter_by(adzuna_id="12345").first()
    assert saved is not None
    assert saved.title == "Test Engineer"
    assert saved.company == "Test Corp"


def test_duplicate_job_is_skipped(monkeypatch, test_session):
    """The same job saved twice should not create a duplicate row."""

    monkeypatch.setattr("collect_jobs.Session", lambda: test_session)

    fake_job = [{
        "id": "99999",
        "title": "Duplicate Job",
        "company": {"display_name": "Dup Corp"},
        "location": {"display_name": "Remote"},
        "description": "Testing duplicates",
        "created": "2026-07-14T08:00:00Z",
        "redirect_url": "https://example.com/job/99999"
    }]

    save_jobs(fake_job)
    save_jobs(fake_job)  # save the exact same job again

    count = test_session.query(JobPosting).filter_by(adzuna_id="99999").count()
    assert count == 1