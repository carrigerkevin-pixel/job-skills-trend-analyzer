import os
import requests
from datetime import date, datetime
from dotenv import load_dotenv
from models import JobPosting, Session
import logging

logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()  # raises an error for 4xx/5xx responses
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch page {page} for '{query}': {e}")
            print(f"Error fetching page {page} for '{query}' — skipping. See pipeline.log for details.")
            break

        data = response.json()
        all_jobs.extend(data.get("results", []))

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

    for query in SEARCH_QUERIES:
        print(f"\nSearching for: {query}")
        logging.info(f"Starting search for '{query}'")

        try:
            jobs = fetch_jobs(query=query, pages=PAGES_PER_QUERY)
            print(f"Fetched {len(jobs)} jobs from API")
            save_jobs(jobs)
        except Exception as e:
            logging.error(f"Unexpected error processing '{query}': {e}")
            print(f"Something went wrong with '{query}' — skipping. See pipeline.log for details.")
            continue