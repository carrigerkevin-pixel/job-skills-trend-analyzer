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

## Known Limitation: Database Sync Across Environments

- The SQLite database (`data/jobs.db`) is tracked in git and shared
  across local development, GitHub Actions automation, and Docker
  builds. This can cause sync conflicts (e.g. an automated CI run
  can overwrite local data, or a stale local commit can overwrite
  CI's data).
- Future improvement: use a proper hosted database (e.g. PostgreSQL
  on a cloud provider) as a single source of truth instead of a
  local file, which would eliminate this class of issue entirely.