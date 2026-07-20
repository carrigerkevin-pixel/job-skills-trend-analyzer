import os
import requests
from datetime import date, datetime
from dotenv import load_dotenv
from models import JobPosting, Session

load_dotenv()

app_id = os.getenv("ADZUNA_APP_ID")
app_key = os.getenv("ADZUNA_APP_KEY")

def fetch_jobs(query="software engineer", pages=1):
    """Fetch jobs from Adzuna for a given search query."""
    all_jobs = []

    for page in range(1, pages + 1):
        url = f"https://api.adzuna.com/v1/api/jobs/us/search/{page}"
        params = {
            "app_id": app_id,
            "app_key": app_key,
            "results_per_page": 20,
            "what": query
        }
        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"Error on page {page}: {response.status_code}")
            break

        data = response.json()
        all_jobs.extend(data["results"])

    return all_jobs


def save_jobs(jobs):
    """Save a list of job dicts into the database, skipping duplicates."""
    session = Session()
    new_count = 0
    skipped_count = 0

    for job in jobs:
        # Check if this job is already in the database
        exists = session.query(JobPosting).filter_by(adzuna_id=job["id"]).first()
        if exists:
            skipped_count += 1
            continue
        posting = JobPosting(
            adzuna_id=job["id"],
            title=job.get("title"),
            company=job.get("company", {}).get("display_name"),
            location=job.get("location", {}).get("display_name"),
            description=job.get("description"),
            date_posted=datetime.strptime(job.get("created", "")[:10], "%Y-%m-%d").date(),
            date_collected=date.today(),
            url=job.get("redirect_url")
        )
        session.add(posting)
        new_count += 1

    session.commit()
    session.close()
    print(f"Saved {new_count} new jobs. Skipped {skipped_count} duplicates.")


if __name__ == "__main__":
    from config import SEARCH_QUERIES, PAGES_PER_QUERY

    total_new = 0

    for query in SEARCH_QUERIES:
        print(f"\nSearching for: {query}")
        jobs = fetch_jobs(query=query, pages=PAGES_PER_QUERY)
        print(f"Fetched {len(jobs)} jobs from API")
        save_jobs(jobs)