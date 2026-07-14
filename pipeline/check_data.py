from models import Session, JobPosting

session = Session()
jobs = session.query(JobPosting).all()

print(f"Total jobs in database: {len(jobs)}")
for job in jobs[:5]:
    print(f"- {job.title} at {job.company} ({job.location})")

session.close()