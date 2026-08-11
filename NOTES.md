# Project Notes

## Known Data Limitations

- Adzuna's free-tier API truncates job descriptions to ~500 characters.
  This means skill extraction only sees the beginning portion of each
  posting, likely undercounting skills mentioned later (e.g. in
  "requirements" or "qualifications" sections).
- Skill trend counts should be read as directional signals based on
  visible text, not exhaustive skill coverage.
- Possible future improvement: scrape full descriptions from the
  `redirect_url` field for a sample of postings.

## Resolved: Database Sync Across Environments

Originally, this project used a local SQLite file tracked in git,
shared across local dev, GitHub Actions, and Docker — which caused
sync conflicts (e.g. an automated run could overwrite local data).

**Fix:** migrated to a hosted PostgreSQL database (Neon). All
environments (local, GitHub Actions, Streamlit Cloud, Docker) now
connect to the same database via a `DATABASE_URL` environment
variable, eliminating sync issues entirely.